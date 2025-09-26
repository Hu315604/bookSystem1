"""
Library Management System - FastAPI Backend
ISYS3001 配置管理和采购管理演示项目
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from datetime import datetime
from typing import List, Optional

from app.models import Book, User, BorrowRecord, BookRequest, UserRequest, ApiResponse, LibraryStats
from app.services import BookService, UserService, BorrowRecordService, StatsService

# 创建FastAPI应用
app = FastAPI(
    title="Library Management System",
    description="ISYS3001 Configuration Management Demo Project - Library Management System",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# 初始化服务
book_service = BookService()
user_service = UserService()
borrow_service = BorrowRecordService()
stats_service = StatsService()

# 首页路由
@app.get("/")
async def read_index():
    """服务前端页面"""
    return FileResponse('frontend/index.html')

@app.get("/books")
async def books_page():
    """图书管理页面"""
    return FileResponse('frontend/index.html')

@app.get("/users")
async def users_page():
    """用户管理页面"""
    return FileResponse('frontend/index.html')

# ============= 健康检查 =============
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return ApiResponse(
        success=True,
        message="Library Management System is running normally",
        data={
            "status": "UP",
            "service": "Library Management System API",
            "version": "1.0.0",
            "timestamp": datetime.now(),
            "description": "ISYS3001 Configuration Management Demo Project - Library Management System"
        }
    )

# ============= 图书管理API =============
@app.get("/api/books", response_model=ApiResponse[List[Book]])
async def get_all_books():
    """Get all books"""
    try:
        books = await book_service.get_all_books()
        return ApiResponse(success=True, message="Books retrieved successfully", data=books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve books: {str(e)}")

@app.get("/api/books/{book_id}", response_model=ApiResponse[Book])
async def get_book_by_id(book_id: int):
    """根据ID获取图书"""
    try:
        book = await book_service.get_book_by_id(book_id)
        if book:
            return ApiResponse(success=True, message="Book retrieved successfully", data=book)
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取图书失败: {str(e)}")

@app.post("/api/books", response_model=ApiResponse[Book])
async def create_book(book_request: BookRequest):
    """创建新图书"""
    try:
        book = await book_service.create_book(book_request)
        return ApiResponse(success=True, message="图书创建成功", data=book)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建图书失败: {str(e)}")

@app.put("/api/books/{book_id}", response_model=ApiResponse[Book])
async def update_book(book_id: int, book_request: BookRequest):
    """更新图书"""
    try:
        book = await book_service.update_book(book_id, book_request)
        if book:
            return ApiResponse(success=True, message="图书更新成功", data=book)
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新图书失败: {str(e)}")

@app.delete("/api/books/{book_id}", response_model=ApiResponse)
async def delete_book(book_id: int):
    """删除图书"""
    try:
        success = await book_service.delete_book(book_id)
        if success:
            return ApiResponse(success=True, message="图书删除成功")
        else:
            raise HTTPException(status_code=404, detail="Book not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除图书失败: {str(e)}")

@app.get("/api/books/search", response_model=ApiResponse[List[Book]])
async def search_books(keyword: str):
    """搜索图书"""
    try:
        books = await book_service.search_books(keyword)
        return ApiResponse(success=True, message="搜索图书成功", data=books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索图书失败: {str(e)}")

@app.get("/api/books/category/{category}", response_model=ApiResponse[List[Book]])
async def get_books_by_category(category: str):
    """根据分类获取图书"""
    try:
        books = await book_service.get_books_by_category(category)
        return ApiResponse(success=True, message="获取分类图书成功", data=books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分类图书失败: {str(e)}")

@app.get("/api/books/available", response_model=ApiResponse[List[Book]])
async def get_available_books():
    """获取可借阅图书"""
    try:
        books = await book_service.get_available_books()
        return ApiResponse(success=True, message="获取可借阅图书成功", data=books)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取可借阅图书失败: {str(e)}")

# ============= 用户管理API =============
@app.get("/api/users", response_model=ApiResponse[List[User]])
async def get_all_users():
    """获取所有用户"""
    try:
        users = await user_service.get_all_users()
        return ApiResponse(success=True, message="获取用户列表成功", data=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")

@app.get("/api/users/{user_id}", response_model=ApiResponse[User])
async def get_user_by_id(user_id: int):
    """根据ID获取用户"""
    try:
        user = await user_service.get_user_by_id(user_id)
        if user:
            return ApiResponse(success=True, message="获取用户成功", data=user)
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户失败: {str(e)}")

@app.post("/api/users", response_model=ApiResponse[User])
async def create_user(user_request: UserRequest):
    """创建新用户"""
    try:
        user = await user_service.create_user(user_request)
        return ApiResponse(success=True, message="用户创建成功", data=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建用户失败: {str(e)}")

@app.put("/api/users/{user_id}", response_model=ApiResponse[User])
async def update_user(user_id: int, user_request: UserRequest):
    """更新用户"""
    try:
        user = await user_service.update_user(user_id, user_request)
        if user:
            return ApiResponse(success=True, message="用户更新成功", data=user)
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")

@app.delete("/api/users/{user_id}", response_model=ApiResponse)
async def delete_user(user_id: int):
    """删除用户"""
    try:
        success = await user_service.delete_user(user_id)
        if success:
            return ApiResponse(success=True, message="用户删除成功")
        else:
            raise HTTPException(status_code=404, detail="用户不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")

@app.get("/api/users/active", response_model=ApiResponse[List[User]])
async def get_active_users():
    """获取活跃用户"""
    try:
        users = await user_service.get_active_users()
        return ApiResponse(success=True, message="获取活跃用户成功", data=users)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取活跃用户失败: {str(e)}")

# ============= 借阅记录API =============
@app.get("/api/borrow-records", response_model=ApiResponse[List[BorrowRecord]])
async def get_all_borrow_records():
    """获取所有借阅记录"""
    try:
        records = await borrow_service.get_all_borrow_records()
        return ApiResponse(success=True, message="获取借阅记录成功", data=records)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取借阅记录失败: {str(e)}")

@app.get("/api/borrow-records/{record_id}", response_model=ApiResponse[BorrowRecord])
async def get_borrow_record_by_id(record_id: int):
    """根据ID获取借阅记录"""
    try:
        record = await borrow_service.get_borrow_record_by_id(record_id)
        if record:
            return ApiResponse(success=True, message="获取借阅记录成功", data=record)
        else:
            raise HTTPException(status_code=404, detail="借阅记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取借阅记录失败: {str(e)}")

@app.post("/api/borrow-records", response_model=ApiResponse[BorrowRecord])
async def create_borrow_record(record: BorrowRecord):
    """创建借阅记录"""
    try:
        created_record = await borrow_service.create_borrow_record(record)
        return ApiResponse(success=True, message="借阅记录创建成功", data=created_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建借阅记录失败: {str(e)}")

@app.patch("/api/borrow-records/{record_id}/return", response_model=ApiResponse[BorrowRecord])
async def return_book(record_id: int):
    """归还图书"""
    try:
        record = await borrow_service.return_book(record_id)
        if record:
            return ApiResponse(success=True, message="图书归还成功", data=record)
        else:
            raise HTTPException(status_code=404, detail="借阅记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"图书归还失败: {str(e)}")

@app.delete("/api/borrow-records/{record_id}", response_model=ApiResponse)
async def delete_borrow_record(record_id: int):
    """删除借阅记录"""
    try:
        success = await borrow_service.delete_borrow_record(record_id)
        if success:
            return ApiResponse(success=True, message="借阅记录删除成功")
        else:
            raise HTTPException(status_code=404, detail="借阅记录不存在")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除借阅记录失败: {str(e)}")

# ============= 统计信息API =============
@app.get("/api/stats", response_model=ApiResponse[LibraryStats])
async def get_library_stats():
    """获取图书馆统计信息"""
    try:
        stats = await stats_service.get_library_stats()
        return ApiResponse(success=True, message="获取统计信息成功", data=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计信息失败: {str(e)}")

# 启动服务器
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║                图书管理系统启动成功                          ║
║                                                            ║
║  🚀 FastAPI服务器: http://localhost:8000                   ║
║  🏥 健康检查: http://localhost:8000/api/health              ║
║  📖 图书API: http://localhost:8000/api/books               ║
║  👤 用户API: http://localhost:8000/api/users               ║
║  📊 API文档: http://localhost:8000/docs                    ║
║                                                            ║
║  ISYS3001 配置管理演示项目 - Python FastAPI版本             ║
╚════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
