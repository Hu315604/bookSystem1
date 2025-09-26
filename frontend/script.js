// Library Management System JavaScript
class LibraryManager {
    constructor() {
        this.books = [];
        this.users = [];
        this.borrowRecords = [];
        this.apiBaseUrl = '/api';
        this.currentTab = 'books';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadAllData();
        this.showTab('books');
    }

    // 绑定事件
    bindEvents() {
        // 标签切换
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.dataset.tab;
                this.showTab(tab);
            });
        });

        // 搜索功能
        document.getElementById('bookSearch').addEventListener('input', () => {
            this.searchBooks();
        });

        // 分类过滤
        document.getElementById('categoryFilter').addEventListener('change', () => {
            this.filterByCategory();
        });

        // 借阅状态过滤
        document.querySelectorAll('.borrow-controls .filter-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.filterBorrowRecords(e.target.dataset.status);
                this.updateFilterButtons(e.target);
            });
        });
    }

    // 显示标签页
    showTab(tabName) {
        // 隐藏所有标签内容
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        // 移除所有标签按钮的active类
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // 显示选中的标签
        document.getElementById(`${tabName}-tab`).classList.add('active');
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        this.currentTab = tabName;

        // 根据标签加载相应数据
        switch (tabName) {
            case 'books':
                this.loadBooks();
                break;
            case 'users':
                this.loadUsers();
                break;
            case 'borrow':
                this.loadBorrowRecords();
                break;
            case 'stats':
                this.loadStats();
                break;
        }
    }

    // 加载所有数据
    async loadAllData() {
        try {
            await Promise.all([
                this.loadBooks(),
                this.loadUsers(),
                this.loadBorrowRecords()
            ]);
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    }

    // 加载图书数据
    async loadBooks() {
        try {
            console.log('Loading books data...');
            const response = await fetch(`${this.apiBaseUrl}/books`);
            console.log('API response status:', response.status);
            const result = await response.json();
            console.log('API response data:', result);
            
            if (result.success) {
                this.books = result.data || [];
                console.log('Successfully loaded books:', this.books.length, 'books');
            } else {
                console.error('Failed to load books:', result.message);
                this.books = [];
                this.showError('Failed to load books data: ' + result.message);
            }
            this.renderBooks();
        } catch (error) {
            console.error('Failed to load books:', error);
            // If API call fails, use dummy data as fallback
            this.books = [
                {
                    id: 1,
                    title: "Python Programming: From Beginner to Advanced",
                    author: "John Smith",
                    isbn: "978-0-123456-78-9",
                    publisher: "Tech Publishing House",
                    publishDate: "2023-01-15",
                    category: {value: "technology", displayName: "Technology"},
                    description: "A comprehensive guide to Python programming for beginners and advanced developers.",
                    totalCopies: 5,
                    availableCopies: 3,
                    status: {value: "available", displayName: "Available"},
                    createdAt: "2024-01-01T10:00:00"
                },
                {
                    id: 2,
                    title: "Algorithm Design Manual",
                    author: "Steven S. Skiena",
                    isbn: "978-7-111-40721-5",
                    publisher: "Engineering Press",
                    publishDate: "2019-06-20",
                    category: {value: "science", displayName: "Science"},
                    description: "Essential algorithms and data structures for computer science students.",
                    totalCopies: 8,
                    availableCopies: 5,
                    status: {value: "available", displayName: "Available"},
                    createdAt: "2024-01-02T10:00:00"
                }
            ];
            this.renderBooks();
            console.log('Using demo data as backup data');
        }
    }

    // 加载用户数据
    async loadUsers() {
        try {
            console.log('Loading users data...');
            const response = await fetch(`${this.apiBaseUrl}/users`);
            console.log('User API response status:', response.status);
            const result = await response.json();
            console.log('User API response data:', result);
            
            if (result.success) {
                this.users = result.data || [];
                console.log('Successfully loaded users:', this.users.length, 'users');
            } else {
                console.error('Failed to load users:', result.message);
                this.users = [];
                this.showError('Failed to load users data: ' + result.message);
            }
            this.renderUsers();
        } catch (error) {
            console.error('Failed to load users:', error);
            // If API call fails, use dummy data as fallback
            this.users = [
                {
                    id: 1,
                    name: "John Doe",
                    email: "john.doe@example.com",
                    phone: "1234567890",
                    userType: {value: "student", displayName: "Student"},
                    status: {value: "active", displayName: "Active"},
                    maxBorrowLimit: 5,
                    currentBorrowCount: 2,
                    registeredAt: "2024-01-01T09:00:00"
                },
                {
                    id: 2,
                    name: "Jane Smith",
                    email: "jane.smith@example.com",
                    phone: "0987654321",
                    userType: {value: "faculty", displayName: "Faculty"},
                    status: {value: "active", displayName: "Active"},
                    maxBorrowLimit: 10,
                    currentBorrowCount: 3,
                    registeredAt: "2024-01-02T09:00:00"
                }
            ];
            this.renderUsers();
            console.log('Using demo data as backup data');
        }
    }

    // 加载借阅记录
    async loadBorrowRecords() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/borrow-records`);
            const result = await response.json();
            
            if (result.success) {
                this.borrowRecords = result.data || [];
            } else {
                console.error('Failed to load borrow records:', result.message);
                this.borrowRecords = [];
                this.showError('Failed to load borrow records: ' + result.message);
            }
            this.renderBorrowRecords();
        } catch (error) {
            console.error('Failed to load borrow records:', error);
            // If API call fails, use dummy data as fallback
            this.borrowRecords = [
                {
                    id: 1,
                    userId: 1,
                    bookId: 1,
                    userName: "John Doe",
                    bookTitle: "Python Programming: From Beginner to Advanced",
                    borrowDate: "2024-09-01",
                    dueDate: "2024-09-30",
                    returnDate: null,
                    status: {value: "borrowed", displayName: "Borrowed"},
                    fine: 0,
                    createdAt: "2024-09-01T10:00:00"
                },
                {
                    id: 2,
                    userId: 2,
                    bookId: 2,
                    userName: "Jane Smith",
                    bookTitle: "Algorithm Design Manual",
                    borrowDate: "2024-08-15",
                    dueDate: "2024-09-15",
                    returnDate: "2024-09-10",
                    status: {value: "returned", displayName: "Returned"},
                    fine: 0,
                    createdAt: "2024-08-15T10:00:00"
                },
                {
                    id: 3,
                    userId: 1,
                    bookId: 3,
                    userName: "John Doe",
                    bookTitle: "The Great Gatsby",
                    borrowDate: "2024-08-01",
                    dueDate: "2024-08-31",
                    returnDate: null,
                    status: {value: "overdue", displayName: "Overdue"},
                    fine: 25,
                    createdAt: "2024-08-01T10:00:00"
                }
            ];
            this.renderBorrowRecords();
            console.log('Using demo data as backup data');
        }
    }

    // 渲染图书列表
    renderBooks(booksToRender = null) {
        const booksList = document.getElementById('booksList');
        const books = booksToRender || this.books;

        if (books.length === 0) {
            booksList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-book-open"></i>
                    <h3>No Books</h3>
                    <p>Click "Add Book" to start managing books</p>
                </div>
            `;
            return;
        }

        booksList.innerHTML = books.map(book => `
            <div class="book-card">
                <div class="book-title">${this.escapeHtml(book.title)}</div>
                <div class="book-author">Author: ${this.escapeHtml(book.author)}</div>
                <div class="book-info">
                    Publisher: ${this.escapeHtml(book.publisher)} | 
                    ISBN: ${book.isbn || 'N/A'}
                </div>
                <div class="book-category category-${book.category?.value || book.category}">
                    ${book.category?.displayName || this.getCategoryDisplayName(book.category)}
                </div>
                <div class="book-info">
                    Stock: ${book.available_copies || book.availableCopies}/${book.total_copies || book.totalCopies} | 
                    Status: ${book.status?.displayName || this.getStatusDisplayName(book.status)}
                </div>
                <div class="card-actions">
                    <button class="btn-secondary" onclick="libraryManager.editBook(${book.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-danger" onclick="libraryManager.deleteBook(${book.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                    ${book.availableCopies > 0 ? 
                        `<button class="btn-primary" onclick="libraryManager.borrowBook(${book.id})">
                            <i class="fas fa-book-reader"></i> Borrow
                        </button>` : ''
                    }
                </div>
            </div>
        `).join('');
    }

    // 渲染用户列表
    renderUsers() {
        const usersList = document.getElementById('usersList');

        if (this.users.length === 0) {
            usersList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-users"></i>
                    <h3>No Users</h3>
                    <p>Click "Add User" to start managing users</p>
                </div>
            `;
            return;
        }

        usersList.innerHTML = this.users.map(user => `
            <div class="user-card">
                <div class="user-name">${this.escapeHtml(user.name)}</div>
                <div class="user-email">${this.escapeHtml(user.email)}</div>
                <div class="user-info">
                    Phone: ${user.phone || 'Not set'} | 
                    Borrowed: ${user.current_borrow_count || user.currentBorrowCount}/${user.max_borrow_limit || user.maxBorrowLimit}
                </div>
                <div class="user-type type-${user.user_type?.value || user.user_type || user.userType?.value}">
                    ${user.user_type?.displayName || user.userType?.displayName || this.getUserTypeDisplayName(user.user_type || user.userType)}
                </div>
                <div class="card-actions">
                    <button class="btn-secondary" onclick="libraryManager.editUser(${user.id})">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-danger" onclick="libraryManager.deleteUser(${user.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </div>
        `).join('');
    }

    // 渲染借阅记录
    renderBorrowRecords(recordsToRender = null) {
        const borrowList = document.getElementById('borrowList');
        const records = recordsToRender || this.borrowRecords;

        if (records.length === 0) {
            borrowList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-exchange-alt"></i>
                    <h3>No Borrow Records</h3>
                    <p>Records will appear here after books are borrowed</p>
                </div>
            `;
            return;
        }

        borrowList.innerHTML = records.map(record => {
            // 处理状态显示
            const statusMap = {
                'borrowed': 'Borrowed',
                'returned': 'Returned', 
                'overdue': 'Overdue',
                'lost': 'Lost',
                'damaged': 'Damaged'
            };
            
            const statusValue = record.status?.value || record.status;
            const statusDisplay = record.status?.displayName || statusMap[statusValue] || statusValue;
            
            // 处理字段名（兼容API返回的snake_case和前端期望的camelCase）
            const bookTitle = record.bookTitle || record.book_title || 'Unknown Book';
            const userName = record.userName || record.user_name || 'Unknown User';
            const borrowDate = record.borrowDate || record.borrow_date || '';
            const dueDate = record.dueDate || record.due_date || '';
            const returnDate = record.returnDate || record.return_date || null;
            
            return `
                <div class="borrow-record">
                    <div class="record-header">
                        <h4>${this.escapeHtml(bookTitle)}</h4>
                        <span class="status-${statusValue}">${statusDisplay}</span>
                    </div>
                    <div class="record-info">
                        <div><strong>Borrower:</strong> ${this.escapeHtml(userName)}</div>
                        <div><strong>Borrow Date:</strong> ${borrowDate}</div>
                        <div><strong>Due Date:</strong> ${dueDate}</div>
                        <div><strong>Return Date:</strong> ${returnDate || 'Not returned'}</div>
                        <div><strong>Fine:</strong> $${record.fine || 0}</div>
                    </div>
                    <div class="card-actions">
                        ${statusValue === 'borrowed' || statusValue === 'overdue' ? 
                            `<button class="btn-primary" onclick="libraryManager.returnBook(${record.id})">
                                <i class="fas fa-undo"></i> Return
                            </button>` : ''
                        }
                        <button class="btn-danger" onclick="libraryManager.deleteBorrowRecord(${record.id})">
                            <i class="fas fa-trash"></i> Delete Record
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }

    // 加载统计信息
    async loadStats() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/stats`);
            const result = await response.json();
            
            if (result.success) {
                const stats = result.data;
                document.getElementById('totalBooks').textContent = stats.totalBooks;
                document.getElementById('availableBooks').textContent = stats.availableBooks;
                document.getElementById('borrowedBooks').textContent = stats.borrowedBooks;
                document.getElementById('totalUsers').textContent = stats.totalUsers;
            } else {
                // 使用本地计算的统计信息作为fallback
                const stats = {
                    totalBooks: this.books.length,
                    availableBooks: this.books.reduce((sum, book) => sum + book.availableCopies, 0),
                    borrowedBooks: this.books.reduce((sum, book) => sum + (book.totalCopies - book.availableCopies), 0),
                    totalUsers: this.users.length
                };

                document.getElementById('totalBooks').textContent = stats.totalBooks;
                document.getElementById('availableBooks').textContent = stats.availableBooks;
                document.getElementById('borrowedBooks').textContent = stats.borrowedBooks;
                document.getElementById('totalUsers').textContent = stats.totalUsers;
            }
        } catch (error) {
            console.error('Failed to load statistics:', error);
            // 使用本地计算的统计信息作为fallback
            const stats = {
                totalBooks: this.books.length,
                availableBooks: this.books.reduce((sum, book) => sum + book.availableCopies, 0),
                borrowedBooks: this.books.reduce((sum, book) => sum + (book.totalCopies - book.availableCopies), 0),
                totalUsers: this.users.length
            };

            document.getElementById('totalBooks').textContent = stats.totalBooks;
            document.getElementById('availableBooks').textContent = stats.availableBooks;
            document.getElementById('borrowedBooks').textContent = stats.borrowedBooks;
            document.getElementById('totalUsers').textContent = stats.totalUsers;
        }
    }

    // 搜索图书
    searchBooks() {
        const keyword = document.getElementById('bookSearch').value.toLowerCase().trim();
        if (!keyword) {
            this.renderBooks();
            return;
        }

        const filteredBooks = this.books.filter(book => 
            book.title.toLowerCase().includes(keyword) ||
            book.author.toLowerCase().includes(keyword) ||
            book.publisher.toLowerCase().includes(keyword)
        );

        this.renderBooks(filteredBooks);
    }

    // 按分类过滤
    filterByCategory() {
        const category = document.getElementById('categoryFilter').value;
        if (!category) {
            this.renderBooks();
            return;
        }

        const filteredBooks = this.books.filter(book => book.category.value === category);
        this.renderBooks(filteredBooks);
    }

    // 过滤借阅记录
    filterBorrowRecords(status) {
        if (status === 'all') {
            this.renderBorrowRecords();
            return;
        }

        const filteredRecords = this.borrowRecords.filter(record => {
            const statusValue = record.status?.value || record.status;
            return statusValue === status;
        });
        this.renderBorrowRecords(filteredRecords);
    }

    // 更新过滤按钮状态
    updateFilterButtons(activeBtn) {
        document.querySelectorAll('.borrow-controls .filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeBtn.classList.add('active');
    }

    // HTML转义
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // 获取分类显示名称
    getCategoryDisplayName(category) {
        const categoryMap = {
            'fiction': 'Fiction',
            'science': 'Science',
            'technology': 'Technology',
            'history': 'History',
            'education': 'Education',
            'biography': 'Biography',
            'children': 'Children',
            'reference': 'Reference',
            'other': 'Other'
        };
        return categoryMap[category] || category;
    }

    // 获取状态显示名称
    getStatusDisplayName(status) {
        const statusMap = {
            'available': 'Available',
            'borrowed': 'Borrowed',
            'maintenance': 'Maintenance',
            'lost': 'Lost',
            'damaged': 'Damaged'
        };
        return statusMap[status] || status;
    }

    // 获取用户类型显示名称
    getUserTypeDisplayName(userType) {
        const userTypeMap = {
            'student': 'Student',
            'faculty': 'Faculty',
            'staff': 'Staff',
            'visitor': 'Visitor'
        };
        return userTypeMap[userType] || userType;
    }

    // 显示错误消息
    showError(message) {
        alert('Error: ' + message);
    }

    // 显示成功消息
    showSuccess(message) {
        alert('Success: ' + message);
    }

    // 模态框操作
    showModal(content) {
        document.getElementById('modalBody').innerHTML = content;
        document.getElementById('modal').style.display = 'block';
    }

    closeModal() {
        document.getElementById('modal').style.display = 'none';
    }

    // 借阅图书
    async borrowBook(bookId) {
        // Should call borrow API here, showing demo message for now
        this.showSuccess('Borrow function demo - Book ID: ' + bookId);
    }

    // 归还图书
    async returnBook(recordId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/borrow-records/${recordId}/return`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const result = await response.json();
            
            if (result.success) {
                await this.loadBorrowRecords(); // Reload borrow records
                this.showSuccess('Book returned successfully');
            } else {
                this.showError('Return failed: ' + result.message);
            }
        } catch (error) {
            console.error('Failed to return book:', error);
            this.showError('Failed to return book: Network error');
        }
    }

    // 编辑图书
    editBook(bookId) {
        this.showAddBookForm(bookId); // 复用添加表单，传入ID表示编辑模式
    }

    // 删除图书
    async deleteBook(bookId) {
        if (confirm('Are you sure you want to delete this book?')) {
            try {
                const response = await fetch(`${this.apiBaseUrl}/books/${bookId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const result = await response.json();
                
                if (result.success) {
                    await this.loadBooks(); // Reload book list
                    this.showSuccess('Book deleted successfully');
                } else {
                    this.showError('Delete failed: ' + result.message);
                }
            } catch (error) {
                console.error('Failed to delete book:', error);
                this.showError('Failed to delete book: Network error');
            }
        }
    }

    // 编辑用户
    editUser(userId) {
        this.showAddUserForm(userId); // 复用添加表单，传入ID表示编辑模式
    }

    // 删除用户
    async deleteUser(userId) {
        if (confirm('确定要删除这个用户吗？')) {
            try {
                const response = await fetch(`${this.apiBaseUrl}/users/${userId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const result = await response.json();
                
                if (result.success) {
                    await this.loadUsers(); // 重新加载用户列表
                    this.showSuccess('用户删除成功');
                } else {
                    this.showError('删除失败: ' + result.message);
                }
            } catch (error) {
                console.error('删除用户失败:', error);
                this.showError('删除用户失败: 网络错误');
            }
        }
    }

    // 删除借阅记录
    async deleteBorrowRecord(recordId) {
        if (confirm('确定要删除这条借阅记录吗？')) {
            try {
                const response = await fetch(`${this.apiBaseUrl}/borrow-records/${recordId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                const result = await response.json();
                
                if (result.success) {
                    await this.loadBorrowRecords(); // 重新加载借阅记录
                    this.showSuccess('借阅记录删除成功');
                } else {
                    this.showError('删除失败: ' + result.message);
                }
            } catch (error) {
                console.error('删除借阅记录失败:', error);
                this.showError('删除借阅记录失败: 网络错误');
            }
        }
    }

    // 显示添加图书表单
    showAddBookForm(bookId = null) {
        const isEdit = bookId !== null;
        const title = isEdit ? 'Edit Book' : 'Add Book';
        
        const formHtml = `
            <h3>${title}</h3>
            <form id="bookForm">
                <div class="form-group">
                    <label>Book Title</label>
                    <input type="text" id="bookTitle" required>
                </div>
                <div class="form-group">
                    <label>Author</label>
                    <input type="text" id="bookAuthor" required>
                </div>
                <div class="form-group">
                    <label>ISBN</label>
                    <input type="text" id="bookIsbn">
                </div>
                <div class="form-group">
                    <label>Publisher</label>
                    <input type="text" id="bookPublisher">
                </div>
                <div class="form-group">
                    <label>Publish Date</label>
                    <input type="date" id="bookPublishDate">
                </div>
                <div class="form-group">
                    <label>Category</label>
                    <select id="bookCategory" required>
                        <option value="fiction">Fiction</option>
                        <option value="science">Science</option>
                        <option value="technology">Technology</option>
                        <option value="history">History</option>
                        <option value="education">Education</option>
                        <option value="biography">Biography</option>
                        <option value="children">Children</option>
                        <option value="reference">Reference</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="bookDescription" rows="3"></textarea>
                </div>
                <div class="form-group">
                    <label>Total Copies</label>
                    <input type="number" id="bookTotalCopies" min="1" value="1" required>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn-primary">
                        ${isEdit ? 'Update' : 'Add'} Book
                    </button>
                    <button type="button" class="btn-secondary" onclick="libraryManager.closeModal()">
                        Cancel
                    </button>
                </div>
            </form>
        `;
        
        this.showModal(formHtml);
        
        // 绑定表单提交事件
        document.getElementById('bookForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitBookForm(isEdit, bookId);
        });
        
        // 如果是编辑模式，填充现有数据
        if (isEdit) {
            this.fillBookForm(bookId);
        }
    }

    // 显示添加用户表单
    showAddUserForm(userId = null) {
        const isEdit = userId !== null;
        const title = isEdit ? 'Edit User' : 'Add User';
        
        const formHtml = `
            <h3>${title}</h3>
            <form id="userForm">
                <div class="form-group">
                    <label>Name</label>
                    <input type="text" id="userName" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="userEmail" required>
                </div>
                <div class="form-group">
                    <label>Phone</label>
                    <input type="tel" id="userPhone">
                </div>
                <div class="form-group">
                    <label>User Type</label>
                    <select id="userType" required>
                        <option value="student">Student</option>
                        <option value="faculty">Faculty</option>
                        <option value="staff">Staff</option>
                        <option value="visitor">Visitor</option>
                    </select>
                </div>
                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button type="submit" class="btn-primary">
                        ${isEdit ? 'Update' : 'Add'} User
                    </button>
                    <button type="button" class="btn-secondary" onclick="libraryManager.closeModal()">
                        Cancel
                    </button>
                </div>
            </form>
        `;
        
        this.showModal(formHtml);
        
        // 绑定表单提交事件
        document.getElementById('userForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitUserForm(isEdit, userId);
        });
        
        // 如果是编辑模式，填充现有数据
        if (isEdit) {
            this.fillUserForm(userId);
        }
    }

    // 提交图书表单
    async submitBookForm(isEdit, bookId) {
        const bookData = {
            title: document.getElementById('bookTitle').value,
            author: document.getElementById('bookAuthor').value,
            isbn: document.getElementById('bookIsbn').value,
            publisher: document.getElementById('bookPublisher').value,
            publishDate: document.getElementById('bookPublishDate').value,
            category: document.getElementById('bookCategory').value,
            description: document.getElementById('bookDescription').value,
            totalCopies: parseInt(document.getElementById('bookTotalCopies').value)
        };

        try {
            const url = isEdit ? `${this.apiBaseUrl}/books/${bookId}` : `${this.apiBaseUrl}/books`;
            const method = isEdit ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bookData)
            });

            const result = await response.json();
            
            if (result.success) {
                await this.loadBooks();
                this.closeModal();
                this.showSuccess(isEdit ? '图书更新成功' : '图书添加成功');
            } else {
                this.showError((isEdit ? '更新' : '添加') + '失败: ' + result.message);
            }
        } catch (error) {
            console.error((isEdit ? '更新' : '添加') + '图书失败:', error);
            this.showError((isEdit ? '更新' : '添加') + '图书失败: 网络错误');
        }
    }

    // 提交用户表单
    async submitUserForm(isEdit, userId) {
        const userData = {
            name: document.getElementById('userName').value,
            email: document.getElementById('userEmail').value,
            phone: document.getElementById('userPhone').value,
            userType: document.getElementById('userType').value
        };

        try {
            const url = isEdit ? `${this.apiBaseUrl}/users/${userId}` : `${this.apiBaseUrl}/users`;
            const method = isEdit ? 'PUT' : 'POST';
            
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });

            const result = await response.json();
            
            if (result.success) {
                await this.loadUsers();
                this.closeModal();
                this.showSuccess(isEdit ? '用户更新成功' : '用户添加成功');
            } else {
                this.showError((isEdit ? '更新' : '添加') + '失败: ' + result.message);
            }
        } catch (error) {
            console.error((isEdit ? '更新' : '添加') + '用户失败:', error);
            this.showError((isEdit ? '更新' : '添加') + '用户失败: 网络错误');
        }
    }

    // 填充图书表单（编辑模式）
    fillBookForm(bookId) {
        const book = this.books.find(b => b.id == bookId);
        if (book) {
            document.getElementById('bookTitle').value = book.title;
            document.getElementById('bookAuthor').value = book.author;
            document.getElementById('bookIsbn').value = book.isbn || '';
            document.getElementById('bookPublisher').value = book.publisher || '';
            document.getElementById('bookPublishDate').value = book.publishDate || '';
            document.getElementById('bookCategory').value = book.category.value;
            document.getElementById('bookDescription').value = book.description || '';
            document.getElementById('bookTotalCopies').value = book.totalCopies;
        }
    }

    // 填充用户表单（编辑模式）
    fillUserForm(userId) {
        const user = this.users.find(u => u.id == userId);
        if (user) {
            document.getElementById('userName').value = user.name;
            document.getElementById('userEmail').value = user.email;
            document.getElementById('userPhone').value = user.phone || '';
            document.getElementById('userType').value = user.userType.value;
        }
    }
}

// 全局函数
function showAddBookForm() {
    libraryManager.showAddBookForm();
}

function showAddUserForm() {
    libraryManager.showAddUserForm();
}

function showBorrowForm() {
    libraryManager.showSuccess('借阅表单功能演示');
}

function closeModal() {
    libraryManager.closeModal();
}

// 初始化应用
const libraryManager = new LibraryManager();

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('Library Management System 已启动');
});
