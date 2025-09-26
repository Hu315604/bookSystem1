"""
数据模型定义
使用Pydantic进行数据验证和序列化
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Any, Generic, TypeVar
from datetime import datetime, date
from enum import Enum

# 泛型类型
T = TypeVar('T')

# ============= 枚举定义 =============
class BookCategory(str, Enum):
    FICTION = "fiction"
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    HISTORY = "history"
    EDUCATION = "education"
    BIOGRAPHY = "biography"
    CHILDREN = "children"
    REFERENCE = "reference"
    OTHER = "other"

class BookStatus(str, Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    MAINTENANCE = "maintenance"
    DISCONTINUED = "discontinued"

class UserType(str, Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    STAFF = "staff"
    VISITOR = "visitor"

class UserStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class BorrowStatus(str, Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"
    LOST = "lost"
    DAMAGED = "damaged"

# ============= 核心模型 =============
class Book(BaseModel):
    """图书模型"""
    id: Optional[int] = None
    title: str = Field(..., min_length=1, description="图书标题")
    author: str = Field(..., min_length=1, description="作者")
    isbn: Optional[str] = Field(None, description="ISBN号码")
    publisher: Optional[str] = Field(None, description="出版社")
    publish_date: Optional[date] = Field(None, description="出版日期")
    category: BookCategory = Field(..., description="图书分类")
    description: Optional[str] = Field(None, description="图书描述")
    total_copies: int = Field(1, ge=1, description="总库存数量")
    available_copies: int = Field(1, ge=0, description="可借阅数量")
    status: BookStatus = Field(BookStatus.AVAILABLE, description="图书状态")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class User(BaseModel):
    """用户模型"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, description="用户姓名")
    email: str = Field(..., description="邮箱地址")
    phone: Optional[str] = Field(None, description="电话号码")
    user_type: UserType = Field(..., description="用户类型")
    status: UserStatus = Field(UserStatus.ACTIVE, description="用户状态")
    max_borrow_limit: int = Field(5, ge=0, description="最大借阅数量")
    current_borrow_count: int = Field(0, ge=0, description="当前借阅数量")
    registered_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BorrowRecord(BaseModel):
    """借阅记录模型"""
    id: Optional[int] = None
    user_id: int = Field(..., description="用户ID")
    book_id: int = Field(..., description="图书ID")
    user_name: str = Field(..., description="用户姓名")
    book_title: str = Field(..., description="图书标题")
    borrow_date: date = Field(..., description="借阅日期")
    due_date: date = Field(..., description="应还日期")
    return_date: Optional[date] = Field(None, description="实际归还日期")
    status: BorrowStatus = Field(BorrowStatus.BORROWED, description="借阅状态")
    fine: float = Field(0.0, ge=0, description="罚金")
    notes: Optional[str] = Field(None, description="备注")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

# ============= 请求模型 =============
class BookRequest(BaseModel):
    """图书创建/更新请求"""
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    publish_date: Optional[date] = None
    category: BookCategory
    description: Optional[str] = None
    total_copies: int = Field(1, ge=1)

class UserRequest(BaseModel):
    """用户创建/更新请求"""
    name: str = Field(..., min_length=1)
    email: str = Field(...)
    phone: Optional[str] = None
    user_type: UserType

# ============= 响应模型 =============
class ApiResponse(BaseModel, Generic[T]):
    """统一API响应格式"""
    success: bool
    message: str
    data: Optional[T] = None
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)
    error_code: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class LibraryStats(BaseModel):
    """图书馆统计信息"""
    total_books: int = Field(0, description="总图书数")
    available_books: int = Field(0, description="可借阅图书数")
    borrowed_books: int = Field(0, description="已借出图书数")
    total_users: int = Field(0, description="总用户数")
    active_users: int = Field(0, description="活跃用户数")
    total_borrow_records: int = Field(0, description="总借阅记录数")
    overdue_records: int = Field(0, description="逾期记录数")
    book_utilization_rate: float = Field(0.0, description="图书利用率")

# ============= 辅助函数 =============
def get_user_type_display_name(user_type: UserType) -> str:
    """获取用户类型显示名称"""
    display_names = {
        UserType.STUDENT: "学生",
        UserType.FACULTY: "教职工",
        UserType.STAFF: "员工",
        UserType.VISITOR: "访客"
    }
    return display_names.get(user_type, "未知")

def get_category_display_name(category: BookCategory) -> str:
    """获取图书分类显示名称"""
    display_names = {
        BookCategory.FICTION: "小说",
        BookCategory.SCIENCE: "科学",
        BookCategory.TECHNOLOGY: "技术",
        BookCategory.HISTORY: "历史",
        BookCategory.EDUCATION: "教育",
        BookCategory.BIOGRAPHY: "传记",
        BookCategory.CHILDREN: "儿童读物",
        BookCategory.REFERENCE: "参考书",
        BookCategory.OTHER: "其他"
    }
    return display_names.get(category, "未知")

def get_user_type_borrow_limit(user_type: UserType) -> int:
    """获取用户类型默认借阅限制"""
    limits = {
        UserType.STUDENT: 5,
        UserType.FACULTY: 10,
        UserType.STAFF: 8,
        UserType.VISITOR: 2
    }
    return limits.get(user_type, 5)
