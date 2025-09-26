"""
业务服务层
处理所有业务逻辑和数据操作
"""

import json
import os
import aiofiles
from typing import List, Optional
from datetime import datetime, date, timedelta
from app.models import (
    Book, User, BorrowRecord, BookRequest, UserRequest, LibraryStats,
    BookCategory, BookStatus, UserType, UserStatus, BorrowStatus,
    get_user_type_borrow_limit
)

# ============= 基础服务类 =============
class BaseService:
    """基础服务类，提供JSON文件操作"""
    
    def __init__(self, data_file: str):
        self.data_file = data_file
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """确保数据目录存在"""
        os.makedirs("data", exist_ok=True)
    
    async def load_data(self) -> List[dict]:
        """从JSON文件加载数据"""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            async with aiofiles.open(self.data_file, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content) if content.strip() else []
        except Exception as e:
            print(f"加载数据失败 {self.data_file}: {e}")
            return []
    
    async def save_data(self, data: List[dict]):
        """保存数据到JSON文件"""
        try:
            async with aiofiles.open(self.data_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2, default=str))
        except Exception as e:
            print(f"保存数据失败 {self.data_file}: {e}")
            raise

# ============= 图书服务 =============
class BookService(BaseService):
    """图书管理服务"""
    
    def __init__(self):
        super().__init__("data/books.json")
        self.next_id = 1
    
    async def _get_next_id(self) -> int:
        """获取下一个ID"""
        books_data = await self.load_data()
        if books_data:
            self.next_id = max(book.get('id', 0) for book in books_data) + 1
        return self.next_id
    
    def _dict_to_book(self, data: dict) -> Book:
        """将字典转换为Book对象"""
        # 处理日期字段
        if isinstance(data.get('publish_date'), str):
            try:
                data['publish_date'] = datetime.fromisoformat(data['publish_date']).date()
            except:
                data['publish_date'] = None
        
        # 处理时间戳字段
        for field in ['created_at', 'updated_at']:
            if isinstance(data.get(field), str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except:
                    data[field] = None
        
        return Book(**data)
    
    def _book_to_dict(self, book: Book) -> dict:
        """将Book对象转换为字典"""
        data = book.dict()
        # 确保日期和时间格式正确
        if data.get('publish_date'):
            data['publish_date'] = data['publish_date'].isoformat() if isinstance(data['publish_date'], date) else data['publish_date']
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].isoformat() if isinstance(data[field], datetime) else data[field]
        return data
    
    async def get_all_books(self) -> List[Book]:
        """获取所有图书"""
        books_data = await self.load_data()
        return [self._dict_to_book(book_data) for book_data in books_data]
    
    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """根据ID获取图书"""
        books_data = await self.load_data()
        for book_data in books_data:
            if book_data.get('id') == book_id:
                return self._dict_to_book(book_data)
        return None
    
    async def create_book(self, book_request: BookRequest) -> Book:
        """创建新图书"""
        # 创建Book对象
        book = Book(
            id=await self._get_next_id(),
            title=book_request.title,
            author=book_request.author,
            isbn=book_request.isbn,
            publisher=book_request.publisher,
            publish_date=book_request.publish_date,
            category=book_request.category,
            description=book_request.description,
            total_copies=book_request.total_copies,
            available_copies=book_request.total_copies,
            status=BookStatus.AVAILABLE,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # 保存到文件
        books_data = await self.load_data()
        books_data.append(self._book_to_dict(book))
        await self.save_data(books_data)
        
        return book
    
    async def update_book(self, book_id: int, book_request: BookRequest) -> Optional[Book]:
        """更新图书"""
        books_data = await self.load_data()
        
        for i, book_data in enumerate(books_data):
            if book_data.get('id') == book_id:
                # 更新字段
                book_data.update({
                    'title': book_request.title,
                    'author': book_request.author,
                    'isbn': book_request.isbn,
                    'publisher': book_request.publisher,
                    'publish_date': book_request.publish_date.isoformat() if book_request.publish_date else None,
                    'category': book_request.category,
                    'description': book_request.description,
                    'total_copies': book_request.total_copies,
                    'updated_at': datetime.now().isoformat()
                })
                
                await self.save_data(books_data)
                return self._dict_to_book(book_data)
        
        return None
    
    async def delete_book(self, book_id: int) -> bool:
        """删除图书"""
        books_data = await self.load_data()
        original_length = len(books_data)
        
        books_data = [book for book in books_data if book.get('id') != book_id]
        
        if len(books_data) < original_length:
            await self.save_data(books_data)
            return True
        return False
    
    async def search_books(self, keyword: str) -> List[Book]:
        """搜索图书"""
        books = await self.get_all_books()
        keyword = keyword.lower()
        
        return [
            book for book in books
            if keyword in book.title.lower() or
               keyword in book.author.lower() or
               (book.publisher and keyword in book.publisher.lower())
        ]
    
    async def get_books_by_category(self, category: str) -> List[Book]:
        """根据分类获取图书"""
        books = await self.get_all_books()
        return [book for book in books if book.category == category]
    
    async def get_available_books(self) -> List[Book]:
        """获取可借阅图书"""
        books = await self.get_all_books()
        return [book for book in books if book.available_copies > 0 and book.status == BookStatus.AVAILABLE]

# ============= 用户服务 =============
class UserService(BaseService):
    """用户管理服务"""
    
    def __init__(self):
        super().__init__("data/users.json")
        self.next_id = 1
    
    async def _get_next_id(self) -> int:
        """获取下一个ID"""
        users_data = await self.load_data()
        if users_data:
            self.next_id = max(user.get('id', 0) for user in users_data) + 1
        return self.next_id
    
    def _dict_to_user(self, data: dict) -> User:
        """将字典转换为User对象"""
        # 处理时间戳字段
        for field in ['registered_at', 'last_active_at']:
            if isinstance(data.get(field), str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except:
                    data[field] = None
        return User(**data)
    
    def _user_to_dict(self, user: User) -> dict:
        """将User对象转换为字典"""
        data = user.dict()
        # 确保时间格式正确
        for field in ['registered_at', 'last_active_at']:
            if data.get(field):
                data[field] = data[field].isoformat() if isinstance(data[field], datetime) else data[field]
        return data
    
    async def get_all_users(self) -> List[User]:
        """获取所有用户"""
        users_data = await self.load_data()
        return [self._dict_to_user(user_data) for user_data in users_data]
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        users_data = await self.load_data()
        for user_data in users_data:
            if user_data.get('id') == user_id:
                return self._dict_to_user(user_data)
        return None
    
    async def create_user(self, user_request: UserRequest) -> User:
        """创建新用户"""
        # 创建User对象
        user = User(
            id=await self._get_next_id(),
            name=user_request.name,
            email=user_request.email,
            phone=user_request.phone,
            user_type=user_request.user_type,
            status=UserStatus.ACTIVE,
            max_borrow_limit=get_user_type_borrow_limit(user_request.user_type),
            current_borrow_count=0,
            registered_at=datetime.now(),
            last_active_at=datetime.now()
        )
        
        # 保存到文件
        users_data = await self.load_data()
        users_data.append(self._user_to_dict(user))
        await self.save_data(users_data)
        
        return user
    
    async def update_user(self, user_id: int, user_request: UserRequest) -> Optional[User]:
        """更新用户"""
        users_data = await self.load_data()
        
        for i, user_data in enumerate(users_data):
            if user_data.get('id') == user_id:
                # 更新字段
                user_data.update({
                    'name': user_request.name,
                    'email': user_request.email,
                    'phone': user_request.phone,
                    'user_type': user_request.user_type,
                    'last_active_at': datetime.now().isoformat()
                })
                
                await self.save_data(users_data)
                return self._dict_to_user(user_data)
        
        return None
    
    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        users_data = await self.load_data()
        original_length = len(users_data)
        
        users_data = [user for user in users_data if user.get('id') != user_id]
        
        if len(users_data) < original_length:
            await self.save_data(users_data)
            return True
        return False
    
    async def get_active_users(self) -> List[User]:
        """获取活跃用户"""
        users = await self.get_all_users()
        return [user for user in users if user.status == UserStatus.ACTIVE]

# ============= 借阅记录服务 =============
class BorrowRecordService(BaseService):
    """借阅记录管理服务"""
    
    def __init__(self):
        super().__init__("data/borrow_records.json")
        self.next_id = 1
    
    async def _get_next_id(self) -> int:
        """获取下一个ID"""
        records_data = await self.load_data()
        if records_data:
            self.next_id = max(record.get('id', 0) for record in records_data) + 1
        return self.next_id
    
    def _dict_to_record(self, data: dict) -> BorrowRecord:
        """将字典转换为BorrowRecord对象"""
        # 处理日期字段
        for field in ['borrow_date', 'due_date', 'return_date']:
            if isinstance(data.get(field), str):
                try:
                    data[field] = datetime.fromisoformat(data[field]).date()
                except:
                    data[field] = None
        
        # 处理时间戳字段
        for field in ['created_at', 'updated_at']:
            if isinstance(data.get(field), str):
                try:
                    data[field] = datetime.fromisoformat(data[field])
                except:
                    data[field] = None
        
        return BorrowRecord(**data)
    
    def _record_to_dict(self, record: BorrowRecord) -> dict:
        """将BorrowRecord对象转换为字典"""
        data = record.dict()
        # 确保日期和时间格式正确
        for field in ['borrow_date', 'due_date', 'return_date']:
            if data.get(field):
                data[field] = data[field].isoformat() if isinstance(data[field], date) else data[field]
        for field in ['created_at', 'updated_at']:
            if data.get(field):
                data[field] = data[field].isoformat() if isinstance(data[field], datetime) else data[field]
        return data
    
    async def get_all_borrow_records(self) -> List[BorrowRecord]:
        """获取所有借阅记录"""
        records_data = await self.load_data()
        return [self._dict_to_record(record_data) for record_data in records_data]
    
    async def get_borrow_record_by_id(self, record_id: int) -> Optional[BorrowRecord]:
        """根据ID获取借阅记录"""
        records_data = await self.load_data()
        for record_data in records_data:
            if record_data.get('id') == record_id:
                return self._dict_to_record(record_data)
        return None
    
    async def create_borrow_record(self, record: BorrowRecord) -> BorrowRecord:
        """创建借阅记录"""
        record.id = await self._get_next_id()
        record.created_at = datetime.now()
        record.updated_at = datetime.now()
        
        # 保存到文件
        records_data = await self.load_data()
        records_data.append(self._record_to_dict(record))
        await self.save_data(records_data)
        
        return record
    
    async def return_book(self, record_id: int) -> Optional[BorrowRecord]:
        """归还图书"""
        records_data = await self.load_data()
        
        for i, record_data in enumerate(records_data):
            if record_data.get('id') == record_id:
                # 更新归还信息
                return_date = date.today()
                due_date = datetime.fromisoformat(record_data['due_date']).date()
                
                # 计算罚金
                fine = 0.0
                if return_date > due_date:
                    overdue_days = (return_date - due_date).days
                    fine = overdue_days * 1.0  # 每天1元罚金
                
                record_data.update({
                    'return_date': return_date.isoformat(),
                    'status': BorrowStatus.RETURNED,
                    'fine': fine,
                    'updated_at': datetime.now().isoformat()
                })
                
                await self.save_data(records_data)
                return self._dict_to_record(record_data)
        
        return None
    
    async def delete_borrow_record(self, record_id: int) -> bool:
        """删除借阅记录"""
        records_data = await self.load_data()
        original_length = len(records_data)
        
        records_data = [record for record in records_data if record.get('id') != record_id]
        
        if len(records_data) < original_length:
            await self.save_data(records_data)
            return True
        return False

# ============= 统计服务 =============
class StatsService:
    """统计信息服务"""
    
    def __init__(self):
        self.book_service = BookService()
        self.user_service = UserService()
        self.borrow_service = BorrowRecordService()
    
    async def get_library_stats(self) -> LibraryStats:
        """获取图书馆统计信息"""
        # 获取所有数据
        books = await self.book_service.get_all_books()
        users = await self.user_service.get_all_users()
        records = await self.borrow_service.get_all_borrow_records()
        
        # 计算统计信息
        total_books = len(books)
        available_books = sum(book.available_copies for book in books)
        total_copies = sum(book.total_copies for book in books)
        borrowed_books = total_copies - available_books
        
        total_users = len(users)
        active_users = len([user for user in users if user.status == UserStatus.ACTIVE])
        
        total_borrow_records = len(records)
        overdue_records = len([
            record for record in records
            if record.status == BorrowStatus.BORROWED and record.due_date < date.today()
        ])
        
        book_utilization_rate = (borrowed_books / total_copies) if total_copies > 0 else 0.0
        
        return LibraryStats(
            total_books=total_books,
            available_books=available_books,
            borrowed_books=borrowed_books,
            total_users=total_users,
            active_users=active_users,
            total_borrow_records=total_borrow_records,
            overdue_records=overdue_records,
            book_utilization_rate=round(book_utilization_rate, 2)
        )
