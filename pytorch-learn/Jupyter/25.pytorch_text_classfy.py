import torch
import torch.nn as nn
import torch.nn.functional as F
import torchtext
from torchtext.datasets import IMDB
#torchtext包含nlp中一些少量的函数和数据库
from torchtext.datasets.imdb import NUM_LINES
from torchtext.data import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.functional import to_map_style_dataset

import sys
import os
import logging
logging.basicConfig(
    level = logging.WARN,
    stream = sys.stdout,
    format = "%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
)

VOCAB_SIZE = 15000
#第一期：编写GCNN模型代码,注意这个不是图网络，而是gated cnn 门控卷积神经网络
class GCNN(nn.Module):
    def __init__(self, vocab_size = VOCAB_SIZE, embedding_dim = 64, num_class = 2):
        super(GCNN, self).__init__()#对父类初始化

        self.embedding_table = nn.Embedding(vocab_size, embedding_dim)
        nn.init.xavier_uniform_(self.embedding_table.weight)
        #对文本使用一维卷积,embedding_dim作为输入通道数，64输出通道，15是kernel
        #步长接近kernel的一半，每次滑动会有一半的交叉
        self.conv_A_1 = nn.Conv1d(embedding_dim, 64, 15, stride = 7)
        self.conv_B_1 = nn.Conv1d(embedding_dim, 64, 15, stride = 7)

        self.conv_A_2 = nn.Conv1d(64, 64, 15, stride = 7)
        self.conv_B_2 = nn.Conv1d(64, 64, 15, stride = 7)

        self.output_linear1 = nn.Linear(64, 128)
        self.output_linear2 = nn.Linear(128, num_class)

    def forward(self, word_index):
        #定义GCN网络的算子操作流程， 基于句子单词ID输入得到分类Logits输出

        #1.通过word_index得到word_embedding
        #word_index shape:[bs, max_seq_len]
        word_embedding = self.embedding_table(word_index) #[bs, max_seq_len, embedding_dim]
        print("word_embedding:",word_embedding.shape)
        #2。编写第一层1D门卷积模块
        word_embedding = word_embedding.transpose(1, 2) #[bs, embedding_dim, max_seq_len]
        A = self.conv_A_1(word_embedding)  #(max_seq_len - kernel) // stride + 1，这里长度对吗？对的
        # print("A_embedding:",A.shape)
        B = self.conv_B_1(word_embedding)
        H = A * torch.sigmoid(B)  #[bs, 64, max_seq_len]
        # print("H_embedding:",H.shape)

        # A = self.conv_A_2(H)
        # print("A2_embedding:",A.shape)
        B = self.conv_B_2(H)
        H = A * torch.sigmoid(B) #[bs, 64, max_seq_len]
        # print("H2_embedding:",H.shape)

        #3. 池化并经过全连接层
        pool_output = torch.mean(H, dim = -1) #平均池化，得到[bs, 64]
        linear1_output = self.output_linear1(pool_output)  #对embedding维度64做映射
        logits = self.output_linear2(linear1_output) #[bs,2]

        return logits

#更简单的embeddingbag+dnn模型
class TextClassificationModel(nn.Module):
    def __init__(self, vocab_size = VOCAB_SIZE, embed_dim = 64, num_class = 2):
        super(TextClassificationModel, self).__init__()
        #embeddingbag得到的embedding是一个二维张量[bs,embedd_dim],把这句话所有单词embedding做平均
        self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse = False)
        self.fc = nn.Linear(embed_dim, num_class)

    def forward(self, token_index):
        embedded = self.embedding(token_index)
        return self.fc(embedded)

#step2 构建IMDB DataLoader
BATCH_SIZE = 64
#train_data_iter是一个迭代器，可以对它遍历
#每个sample是一个包含标签和数据的元组
#返回的也是一个生成器
def yield_tokens(train_data_iter, tokenizer):
    for i, sample in enumerate(train_data_iter):
        label, comment = sample
        #tokenizer的一个固定用法，可以记住，把一句话变成一个token列表
        yield tokenizer(comment)

#dataset对象两种类型，这里是迭代型，另一种map style推荐后者
train_data_iter = IMDB(root = '.data', split = 'train') #Dataset类型的对象,下载到.data里面，下载训练集部分
#基于这个数据集构建单词表
#实例化一个分词器
tokenizer = get_tokenizer("basic_english")
#传入函数，只考虑出现次数大于20的token，小于20的全部替换成unk
vocab = build_vocab_from_iterator(yield_tokens(train_data_iter, tokenizer), min_freq = 20, specials = ["<unk>"])
#unk设置成0索引
vocab.set_default_index(0)
#这里算出来词表大小就是13351
print( f"单词表大小:{len(vocab)}")

#对data_loader生成的mini-batch进行后处理，把影评文本转化成索引，padding到相同长度，对标签pos/neg转化从0，1
#batch是什么样的要根据dataset返回的是什么来确定
#自己写dataset在get_item返回的是一个(x,y)元组的话，那么接下来对batch遍历返回也是一个（x,y）元组
#与Get_itm的区别在于，这里接收的batch_size个元组，之前返回一个元组
def collate_fn(batch):
    target = []
    token_index = []
    max_length = 0
    for i, (label, comment) in  enumerate(batch):
        tokens = tokenizer(comment)  #首先分词
        token_index.append(vocab(tokens)) #得到Token对应的索引，索引列表添加到token_index
        if len(tokens) > max_length:  #找到最大长度的句子，每个batch最大句子长度不一定一样
            max_length = len(tokens)
        
        if label == "pos":
            target.append(0)
        else:
            target.append(1)
    
    token_index = [index + [0] * (max_length - len(index)) for index in token_index] #padding索引0填充
    #target转化成int64,之后做loss，要先把它转化成one-hot的向量，接受的是长整型数据。token_index是embedding输入
    return (torch.tensor(target).to(torch.int64), torch.tensor(token_index).to(torch.int32))

# step3.编写训练代码
'''
此处dataloader是map_style dataset
log_step_interval:多少次打印一次日志
save_step_interval:多少步保存一次模型参数和优化器输入
eval_step_interval：多少次做一次验证集推理
resue:是否要导入一个已经训练好的模型接着训练
'''
def train(train_data_loader, eval_data_loader, model, optimizer, num_epoch, log_step_interval\
    ,save_step_interval, eval_step_interval, save_path, resume = ""):
    start_epoch = 0
    start_step = 0
    if resume != "":
        #加载之前训练过的模型参数文件
        logging.warning(f"loading from {resume}")
        checkpoint = torch.load(resume)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        start_epoch = checkpoint['epoch']
        start_step = checkpoint['step'] #恢复到上次训练的start_step
    
    #对周期循环
    for epoch_index in  range(start_epoch, num_epoch): 
        ema_loss = 0.   #exp moving average在每个周期里面用指数移动平均的loss来看损失变化情况，而不是用单步loss，震荡太大
        num_batches = len(train_data_loader)

        #对dataloader进行遍历，每次返回一个batch_size的数量
        for batch_index, (target, token_index) in enumerate(train_data_loader):
            optimizer.zero_grad()
            step = num_batches * (epoch_index) + batch_index + 1 #当前多少个batch
            logits = model(token_index)
            bce_loss = F.binary_cross_entropy(torch.sigmoid(logits), F.one_hot(target, num_classes = 2).to(torch.float32))
            ema_loss = 0.9 * ema_loss + 0.1 * bce_loss
            bce_loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 0.1)#对梯度的模长进行截断成最大值0.1，防止梯度消失爆炸
            optimizer.step()

            if step % log_step_interval == 0:
                logging.warning(f"epoch_index: {epoch_index}, batch_index: {batch_index}, ema_loss: {ema_loss.item()}")#转成python类型，性能更好

            if step % save_step_interval == 0:
                os.makedirs(save_path, exist_ok = True)
                save_file = os.path.join(save_path, f"step_{step}.pt")
                torch.save({
                    'epoch': epoch_index,
                    'step':step,
                    'model_state_dict':model.state_dict(),
                    'optimizer_state_dict':optimizer.state_dict(),
                    'loss': bce_loss,
                }, save_file)
                logging.warning(f"checkpoint has been saved in {save_file}")
            
            if step % eval_step_interval == 0:
                logging.warning("start to do evaluation...")
                #注意这里要调用model.eval()函数
                model.eval()
                ema_eval_loss = 0
                total_acc_account = 0
                total_account = 0
                for eval_batch_index, (eval_target, eval_token_index) in enumerate(eval_data_loader):
                    total_account += eval_target.shape[0]
                    eval_logits = model(eval_token_index)
                    total_acc_account += (torch.argmax(eval_logits, dim = -1) == eval_target).sum().item()
                    eval_bec_loss = F.binary_cross_entropy(torch.sigmoid(eval_logits), F.one_hot(eval_target, num_classes=2).to(torch.float32))
                    ema_eval_loss = 0.9*ema_eval_loss + 0.1 * eval_bec_loss
                acc = total_acc_account/total_account
                logging.warning(f"eval_ema_loss:{ema_eval_loss.item()}, eval_acc: {acc.item()}")
                model.train() #下次训练时训练模式


#step4测试代码
if __name__ == "__main__":
    model = GCNN() #参数更大，1214594
    #model = TextClassificationModel()
    print("模型总参数：",sum(p.numel() for p in model.parameters()))
    optimizer = torch.optim.Adam(model.parameters(), lr = 0.001)

    train_data_iter = IMDB(root = '.data', split = 'train') #dataset类型的对象
    '''dataloader可以接收两种类型的数据库，map_style更好，因为迭代型的迭代完成就空了
    下面我们转换成map_style,每轮epoch后dataloader就重新打乱索引，送入map_style dataset中
    '''
    train_data_loader = torch.utils.data.DataLoader(to_map_style_dataset(train_data_iter), batch_size = BATCH_SIZE,\
        collate_fn = collate_fn, shuffle = True)
    
    eval_data_iter = IMDB(root = '.data', split = 'test')
    eval_data_loader = torch.utils.data.DataLoader(to_map_style_dataset(eval_data_iter), batch_size=8, collate_fn = collate_fn)
    resume = ""
    #resume = "D:/Notes/logs_imdb_text_classification/step_500.pt"

    train(train_data_loader, eval_data_loader, model, optimizer, num_epoch=10, log_step_interval=20,\
         save_step_interval=500, eval_step_interval = 300, save_path = "./logs_imdb_text_classification", resume = resume)
    

