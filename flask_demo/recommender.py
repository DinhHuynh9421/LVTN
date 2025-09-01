# file: recommender.py

import torch
import pickle
import numpy as np

# Định nghĩa lại kiến trúc model SASRecPT giống như khi train
# (Phải có ở đây để PyTorch biết cách tải trọng số vào model)

class TransformerBlock(torch.nn.Module):
    def __init__(self, embed_dim, num_heads, dropout=0.1):
        super().__init__()
        self.attn = torch.nn.MultiheadAttention(
            embed_dim, num_heads, dropout=dropout, batch_first=True)
        self.ln1 = torch.nn.LayerNorm(embed_dim)
        self.ffn = torch.nn.Sequential(
            torch.nn.Linear(embed_dim, embed_dim * 4),
            torch.nn.GELU(),
            torch.nn.Linear(embed_dim * 4, embed_dim),
        )
        self.ln2 = torch.nn.LayerNorm(embed_dim)
        self.dropout = torch.nn.Dropout(dropout)
    
    def forward(self, x, attn_mask=None, key_padding_mask=None):
        attn_out, _ = self.attn(
            x, x, x, 
            attn_mask=attn_mask, 
            key_padding_mask=key_padding_mask,
            need_weights=False
        )
        x = self.ln1(x + self.dropout(attn_out))
        ff_out = self.ffn(x)
        x = self.ln2(x + self.dropout(ff_out))
        return x

class SASRecPT(torch.nn.Module):
    def __init__(self, num_items, max_len, embed_dim=64, num_heads=2, num_blocks=1, pad_idx=None, dropout=0.1):
        super().__init__()
        self.num_items = num_items
        self.max_len = max_len
        self.pad_idx = pad_idx if pad_idx is not None else num_items - 1

        self.item_embedding = torch.nn.Embedding(num_items, embed_dim, padding_idx=self.pad_idx)
        self.pos_embedding = torch.nn.Embedding(max_len, embed_dim)
        self.dropout = torch.nn.Dropout(dropout)

        self.blocks = torch.nn.ModuleList([
            TransformerBlock(embed_dim, num_heads, dropout=dropout) 
            for _ in range(num_blocks)
        ])
        
        self.proj = torch.nn.Linear(embed_dim, num_items)
        
        self._init_weights()
    
    def _init_weights(self):
        torch.nn.init.xavier_uniform_(self.item_embedding.weight)
        torch.nn.init.xavier_uniform_(self.pos_embedding.weight)
        torch.nn.init.xavier_uniform_(self.proj.weight)
    
    def _generate_causal_mask(self, L, device):
        mask = torch.full((L, L), float('-inf'), device=device)
        mask = torch.triu(mask, diagonal=1)
        return mask
    
    def forward(self, x):
        B, L = x.shape
        device = x.device
        key_padding_mask = (x == self.pad_idx)
        
        positions = torch.arange(L, device=device).unsqueeze(0).expand(B, L)
        x = self.item_embedding(x) + self.pos_embedding(positions)
        x = self.dropout(x)
        
        attn_mask = self._generate_causal_mask(L, device)
        
        for block in self.blocks:
            x = block(x, attn_mask=attn_mask, key_padding_mask=key_padding_mask)
        
        last_output = x[:, -1, :]
        logits = self.proj(last_output)
        return logits

# Class chính để sử dụng model
class SASRecRecommender:
    def __init__(self, model_path, item_map_path, params_path, device='cpu'):
        self.device = device
        self.params = self._load_params(params_path)
        self.itemid_to_idx = self._load_item_map(item_map_path)
        self.model = self._load_model(model_path) # <-- Đã sửa
        
        self.idx_to_itemid = {v: k for k, v in self.itemid_to_idx.items()}
        self.pad_idx = self.itemid_to_idx['<PAD>']
        self.max_len = self.params['MAX_SESSION_LEN']
        
    def _load_model(self, model_path):
        # Định nghĩa lại kiến trúc model giống như khi train
        # Dùng các tham số đã tải từ params và item_map
        model = SASRecPT(
            num_items=len(self.itemid_to_idx), # <-- SỬA LỖI Ở ĐÂY
            max_len=self.params['MAX_SESSION_LEN'],
            embed_dim=self.params['EMBEDDING_DIM'],
            num_heads=self.params['NUM_HEADS'],
            num_blocks=self.params['NUM_BLOCKS'],
            pad_idx=self.params['PAD_IDX'],
            dropout=self.params.get('DROPOUT_RATE', 0.1)
        )
        
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model.to(self.device)
        model.eval()
        return model
    
    def _load_item_map(self, item_map_path):
        with open(item_map_path, 'rb') as f:
            return pickle.load(f)
    
    def _load_params(self, params_path):
        with open(params_path, 'rb') as f:
            return pickle.load(f)
    
    def recommend(self, session_items, k=5):
        # Chuyển item_id sang index
        seq = [self.itemid_to_idx[item] for item in session_items if item in self.itemid_to_idx]
        
        # Xử lý sequence quá dài hoặc quá ngắn
        if len(seq) > self.max_len:
            seq = seq[-self.max_len:]
        elif len(seq) < self.max_len:
            seq = [self.pad_idx] * (self.max_len - len(seq)) + seq
        
        # Dự đoán
        with torch.no_grad():
            input_tensor = torch.LongTensor([seq]).to(self.device)
            logits = self.model(input_tensor)
            scores = torch.softmax(logits, dim=1).cpu().numpy()[0]
        
        # Loại bỏ các item đã xem
        viewed_indices = [self.itemid_to_idx[item] for item in session_items if item in self.itemid_to_idx]
        scores[viewed_indices] = -np.inf
        scores[self.pad_idx] = -np.inf # Không gợi ý item PAD

        # Lấy top K item
        top_indices = np.argsort(scores)[-k:][::-1]
        
        return [self.idx_to_itemid[idx] for idx in top_indices if idx in self.idx_to_itemid]