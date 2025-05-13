
# **資料庫設置與使用指南**

本文件詳細說明如何設置和使用與 MySQL 資料庫相關的部分，包括模型定義、資料庫初始化和連線管理。

---

## **目錄**
1. 環境需求
2. 資料庫結構
3. 資料庫初始化
4. 資料庫連線
5. 資料庫操作範例
6. 注意事項

---

## **1. 環境需求**

在開始之前，請確保已安裝以下工具與套件：
- **MySQL 資料庫**：版本 5.7 或以上。
- **Python**：版本 3.9 或以上。
- **必要套件**：
  - [`fastapi`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A5%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")
  - [`sqlalchemy`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A5%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A5%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fbase.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A5%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A5%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")
  - [`asyncmy`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A22%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")
  - `pydantic`
  - `python-decouple`（可選，用於管理環境變數）

安裝必要套件：
```bash
pip install fastapi sqlalchemy asyncmy pydantic python-decouple
```

---

## **2. 資料庫結構**

資料庫結構定義在 [`models.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "/Users/hnnch1i/Desktop/111502502/專案/k8s-cicd-automation/backend/src/db/models.py") 中，使用 SQLAlchemy 的 ORM 進行建模。以下是主要的資料表結構：

### **[`User`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A24%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表**
- **用途**：儲存用戶資訊。
- **欄位**：
  - [`id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A30%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：主鍵，自動遞增。
  - [`username`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A16%2C%22character%22%3A32%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A8%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：用戶名，唯一且不可為空。
  - [`nickname`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A36%2C%22character%22%3A31%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：用戶暱稱，可選。

### **[`Game`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表**
- **用途**：儲存遊戲資訊。
- **欄位**：
  - [`id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A30%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：主鍵，自動遞增。
  - [`name`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A15%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：遊戲名稱，不可為空。
  - [`players`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A16%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A26%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：與 [`GamePlayer`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A18%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表的關聯。

### **[`GamePlayer`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A18%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表**
- **用途**：儲存遊戲玩家資訊。
- **欄位**：
  - [`id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A27%2C%22character%22%3A30%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：主鍵，自動遞增。
  - [`game_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A22%2C%22character%22%3A4%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A9%2C%22character%22%3A14%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：外鍵，指向 [`Game`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表。
  - [`user_id`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A28%2C%22character%22%3A28%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A23%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：外鍵，指向 [`User`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A24%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A6%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 表。
  - [`score`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fmodels.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A24%2C%22character%22%3A4%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")：玩家分數，預設為 0。

---

## **3. 資料庫初始化**

資料庫初始化邏輯定義在 [`base.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fbase.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "/Users/hnnch1i/Desktop/111502502/專案/k8s-cicd-automation/backend/src/db/base.py") 中，負責根據模型自動創建資料表。

### **初始化程式碼**
在應用啟動時，執行以下程式碼以初始化資料庫結構：
```python
from sqlalchemy.ext.asyncio import create_async_engine
from .base import init_db

DATABASE_URL = "mysql+asyncmy://kahoot_user:your_password@localhost/kahoot_db"
engine = create_async_engine(DATABASE_URL, echo=True)

async def initialize_database():
    await init_db(engine)
```

### **FastAPI 啟動時初始化**
在 `main.py` 中加入以下邏輯：
```python
from fastapi import FastAPI
from .db.base import init_db
from .db.session import engine

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db(engine)
```

---

## **4. 資料庫連線**

資料庫連線邏輯定義在 [`session.py`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "/Users/hnnch1i/Desktop/111502502/專案/k8s-cicd-automation/backend/src/db/session.py") 中，使用 SQLAlchemy 的非同步引擎進行管理。

### **主要元件**
1. **[`engine`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fbase.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A18%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A5%2C%22character%22%3A0%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")**：
   - 建立與資料庫的非同步連線。
   - 使用 [`create_async_engine`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A35%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 方法，並指定資料庫的連線字串。
   - 範例：
     ```python
     engine = create_async_engine(DATABASE_URL, echo=True)
     ```

2. **[`AsyncSessionLocal`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A7%2C%22character%22%3A0%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")**：
   - 使用 [`sessionmaker`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A1%2C%22character%22%3A27%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 創建非同步的資料庫會話工廠。
   - 範例：
     ```python
     AsyncSessionLocal = sessionmaker(
         bind=engine,
         class_=AsyncSession,
         expire_on_commit=False
     )
     ```

3. **[`get_db`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A25%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A10%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition")**：
   - 定義一個 FastAPI 的 Dependency，用於在請求期間提供資料庫會話。
   - 範例：
     ```python
     async def get_db():
         async with AsyncSessionLocal() as session:
             yield session
     ```

---

## **5. 資料庫操作範例**

以下是一些常見的資料庫操作範例，展示如何使用 SQLAlchemy 與資料庫互動。

### **新增資料**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User

async def create_user(db: AsyncSession, username: str, nickname: str = None):
    new_user = User(username=username, nickname=nickname)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
```

### **查詢資料**
```python
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar()
```

### **更新資料**
```python
async def update_user_nickname(db: AsyncSession, user_id: int, nickname: str):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if user:
        user.nickname = nickname
        await db.commit()
        await db.refresh(user)
    return user
```

### **刪除資料**
```python
async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar()
    if user:
        await db.delete(user)
        await db.commit()
    return user
```

---

## **6. 注意事項**

1. **資料庫連線字串**：
   - 請確保 [`DATABASE_URL`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A3%2C%22character%22%3A0%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 的格式正確，例如：
     ```
     mysql+asyncmy://username:password@host:port/database
     ```
   - 建議使用 [`.env`](command:_github.copilot.openRelativePath?%5B%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2F.env%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "/Users/hnnch1i/Desktop/111502502/專案/k8s-cicd-automation/.env") 檔案管理環境變數，並透過 `python-decouple` 或 `pydantic` 加載。

2. **非同步操作**：
   - 本專案使用 SQLAlchemy 的非同步功能，請確保所有資料庫操作都在 [`async`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fapi%2Froutes.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A13%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fbase.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A0%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fsession.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A14%2C%22character%22%3A0%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 函式中執行。

3. **資料庫初始化**：
   - 在應用啟動時，務必執行 [`init_db`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Fhnnch1i%2FDesktop%2F111502502%2F%E5%B0%88%E6%A1%88%2Fk8s-cicd-automation%2Fbackend%2Fsrc%2Fdb%2Fbase.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A4%2C%22character%22%3A10%7D%7D%5D%2C%2241e7e390-1ba5-42d1-85aa-eb91d0cafe20%22%5D "Go to definition") 函式以確保資料表結構正確。

4. **測試資料庫連線**：
   - 在開發環境中，建議加入測試資料庫連線的邏輯，確保資料庫可用。
   - 範例：
     ```python
     @app.on_event("startup")
     async def test_db_connection():
         try:
             async with engine.begin() as conn:
                 await conn.execute("SELECT 1")
         except Exception as e:
             print("資料庫連線失敗:", e)
             raise e
     ```

5. **錯誤處理**：
   - 在資料庫操作中，請加入適當的錯誤處理邏輯，例如處理連線失敗或查詢不到資料的情況。