"""
Test samples for Danis's Powerful Guess Lexer
Comprehensive test cases for various languages and frameworks
"""

TEST_SAMPLES = {
    'python_basic': {
        'code': '''
def calculate_fibonacci(n: int) -> int:
    """Calculate fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

if __name__ == "__main__":
    print(f"Fibonacci(10) = {calculate_fibonacci(10)}")
''',
        'expected_language': 'python',
        'filename': 'fibonacci.py'
    },
    
    'python_django': {
        'code': '''
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.slug])
    
    def __str__(self):
        return self.title
''',
        'expected_language': 'python',
        'expected_framework': 'django',
        'filename': 'models.py'
    },
    
    'python_flask': {
        'code': '''
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET', 'POST'])
def users_api():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'status': 'created'})
    return jsonify({'users': []})

if __name__ == '__main__':
    app.run(debug=True)
''',
        'expected_language': 'python',
        'expected_framework': 'flask',
        'filename': 'app.py'
    },
    
    'javascript_basic': {
        'code': '''
const users = [
    { id: 1, name: 'John Doe', email: 'john@example.com' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com' }
];

function getUserById(id) {
    return users.find(user => user.id === id);
}

const processUsers = async () => {
    try {
        const userData = await fetch('/api/users');
        const users = await userData.json();
        console.log('Users loaded:', users);
    } catch (error) {
        console.error('Error loading users:', error);
    }
};

module.exports = { getUserById, processUsers };
''',
        'expected_language': 'javascript',
        'filename': 'users.js'
    },
    
    'javascript_react': {
        'code': '''
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get('/api/users');
                setUsers(response.data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, []);

    if (loading) return <div className="spinner">Loading...</div>;
    if (error) return <div className="error">Error: {error}</div>;

    return (
        <div className="user-list">
            {users.map(user => (
                <div key={user.id} className="user-card">
                    <h3>{user.name}</h3>
                    <p>{user.email}</p>
                </div>
            ))}
        </div>
    );
};

export default UserList;
''',
        'expected_language': 'javascript',
        'expected_framework': 'react',
        'filename': 'UserList.jsx'
    },
    
    'typescript_basic': {
        'code': '''
interface User {
    id: number;
    name: string;
    email: string;
    isActive?: boolean;
}

interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}

class UserService {
    private apiUrl: string = '/api/users';

    async getUsers(): Promise<ApiResponse<User[]>> {
        try {
            const response = await fetch(this.apiUrl);
            const data: ApiResponse<User[]> = await response.json();
            return data;
        } catch (error) {
            throw new Error(`Failed to fetch users: ${error}`);
        }
    }

    async createUser(userData: Omit<User, 'id'>): Promise<ApiResponse<User>> {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        return response.json();
    }
}

export { User, UserService };
''',
        'expected_language': 'typescript',
        'filename': 'userService.ts'
    },
    
    'java_basic': {
        'code': '''
package com.example.app;

import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

public class UserManager {
    private List<User> users;
    
    public UserManager() {
        this.users = new ArrayList<>();
    }
    
    public void addUser(User user) {
        if (user != null && user.isValid()) {
            users.add(user);
            System.out.println("User added: " + user.getName());
        }
    }
    
    public List<User> getActiveUsers() {
        return users.stream()
                   .filter(User::isActive)
                   .collect(Collectors.toList());
    }
    
    public static void main(String[] args) {
        UserManager manager = new UserManager();
        User user = new User("John Doe", "john@example.com");
        manager.addUser(user);
        
        System.out.println("Active users: " + manager.getActiveUsers().size());
    }
}
''',
        'expected_language': 'java',
        'filename': 'UserManager.java'
    },
    
    'csharp_basic': {
        'code': '''
using System;
using System.Collections.Generic;
using System.Linq;

namespace UserManagement
{
    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
        public bool IsActive { get; set; }
        
        public User(string name, string email)
        {
            Name = name;
            Email = email;
            IsActive = true;
        }
    }
    
    public class UserService
    {
        private List<User> _users = new List<User>();
        
        public void AddUser(User user)
        {
            if (user != null)
            {
                _users.Add(user);
                Console.WriteLine($"User added: {user.Name}");
            }
        }
        
        public IEnumerable<User> GetActiveUsers()
        {
            return _users.Where(u => u.IsActive);
        }
    }
    
    class Program
    {
        static void Main(string[] args)
        {
            var service = new UserService();
            var user = new User("John Doe", "john@example.com");
            service.AddUser(user);
            
            Console.WriteLine($"Active users: {service.GetActiveUsers().Count()}");
        }
    }
}
''',
        'expected_language': 'csharp',
        'filename': 'UserService.cs'
    },
    
    'cpp_basic': {
        'code': '''
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

class User {
private:
    int id;
    std::string name;
    std::string email;
    bool active;

public:
    User(int id, const std::string& name, const std::string& email) 
        : id(id), name(name), email(email), active(true) {}
    
    int getId() const { return id; }
    std::string getName() const { return name; }
    bool isActive() const { return active; }
    
    void setActive(bool status) { active = status; }
};

class UserManager {
private:
    std::vector<User> users;

public:
    void addUser(const User& user) {
        users.push_back(user);
        std::cout << "User added: " << user.getName() << std::endl;
    }
    
    std::vector<User> getActiveUsers() const {
        std::vector<User> activeUsers;
        std::copy_if(users.begin(), users.end(), 
                     std::back_inserter(activeUsers),
                     [](const User& u) { return u.isActive(); });
        return activeUsers;
    }
};

int main() {
    UserManager manager;
    User user(1, "John Doe", "john@example.com");
    manager.addUser(user);
    
    std::cout << "Active users: " << manager.getActiveUsers().size() << std::endl;
    return 0;
}
''',
        'expected_language': 'cpp',
        'filename': 'main.cpp'
    },
    
    'go_basic': {
        'code': '''
package main

import (
    "fmt"
    "log"
    "net/http"
    "encoding/json"
)

type User struct {
    ID     int    `json:"id"`
    Name   string `json:"name"`
    Email  string `json:"email"`
    Active bool   `json:"active"`
}

type UserService struct {
    users []User
}

func NewUserService() *UserService {
    return &UserService{
        users: make([]User, 0),
    }
}

func (s *UserService) AddUser(user User) {
    s.users = append(s.users, user)
    fmt.Printf("User added: %s\\n", user.Name)
}

func (s *UserService) GetActiveUsers() []User {
    var activeUsers []User
    for _, user := range s.users {
        if user.Active {
            activeUsers = append(activeUsers, user)
        }
    }
    return activeUsers
}

func (s *UserService) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "application/json")
    
    switch r.Method {
    case http.MethodGet:
        users := s.GetActiveUsers()
        json.NewEncoder(w).Encode(users)
    default:
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
    }
}

func main() {
    service := NewUserService()
    user := User{ID: 1, Name: "John Doe", Email: "john@example.com", Active: true}
    service.AddUser(user)
    
    http.Handle("/users", service)
    log.Println("Server starting on :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
''',
        'expected_language': 'go',
        'filename': 'main.go'
    },
    
    'rust_basic': {
        'code': '''
#[derive(Debug, Clone)]
pub struct User {
    pub id: u32,
    pub name: String,
    pub email: String,
    pub active: bool,
}

impl User {
    pub fn new(id: u32, name: String, email: String) -> Self {
        User {
            id,
            name,
            email,
            active: true,
        }
    }
    
    pub fn is_active(&self) -> bool {
        self.active
    }
    
    pub fn set_active(&mut self, active: bool) {
        self.active = active;
    }
}

pub struct UserService {
    users: Vec<User>,
}

impl UserService {
    pub fn new() -> Self {
        UserService {
            users: Vec::new(),
        }
    }
    
    pub fn add_user(&mut self, user: User) {
        println!("User added: {}", user.name);
        self.users.push(user);
    }
    
    pub fn get_active_users(&self) -> Vec<&User> {
        self.users
            .iter()
            .filter(|user| user.is_active())
            .collect()
    }
}

fn main() {
    let mut service = UserService::new();
    let user = User::new(1, "John Doe".to_string(), "john@example.com".to_string());
    service.add_user(user);
    
    println!("Active users: {}", service.get_active_users().len());
}
''',
        'expected_language': 'rust',
        'filename': 'main.rs'
    },
    
    'sql_basic': {
        'code': '''
-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Create posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com');

-- Query active users with their post counts
SELECT 
    u.id,
    u.name,
    u.email,
    COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.name, u.email
HAVING COUNT(p.id) > 0
ORDER BY post_count DESC;

-- Update user status
UPDATE users 
SET is_active = FALSE, updated_at = CURRENT_TIMESTAMP 
WHERE email = 'john@example.com';

-- Delete inactive users
DELETE FROM users 
WHERE is_active = FALSE 
AND created_at < CURRENT_TIMESTAMP - INTERVAL '30 days';
''',
        'expected_language': 'sql',
        'filename': 'schema.sql'
    },
    
    'html_basic': {
        'code': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <header class="navbar">
        <h1>User Management</h1>
        <nav>
            <a href="#dashboard">Dashboard</a>
            <a href="#users">Users</a>
            <a href="#settings">Settings</a>
        </nav>
    </header>
    
    <main class="container">
        <section id="dashboard">
            <h2>Dashboard</h2>
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Users</h3>
                    <span id="user-count">Loading...</span>
                </div>
                <div class="stat-card">
                    <h3>Active Sessions</h3>
                    <span id="session-count">Loading...</span>
                </div>
            </div>
        </section>
        
        <section id="users">
            <h2>User List</h2>
            <button onclick="loadUsers()" class="btn btn-primary">Refresh</button>
            <div id="user-list" class="user-grid">
                <!-- Users will be loaded here -->
            </div>
        </section>
    </main>
    
    <script>
        async function loadUsers() {
            try {
                const response = await axios.get('/api/users');
                displayUsers(response.data);
            } catch (error) {
                console.error('Error loading users:', error);
            }
        }
        
        function displayUsers(users) {
            const container = document.getElementById('user-list');
            container.innerHTML = users.map(user => `
                <div class="user-card">
                    <h3>${user.name}</h3>
                    <p>${user.email}</p>
                    <span class="status ${user.active ? 'active' : 'inactive'}">
                        ${user.active ? 'Active' : 'Inactive'}
                    </span>
                </div>
            `).join('');
        }
        
        // Load users when page loads
        document.addEventListener('DOMContentLoaded', loadUsers);
    </script>
</body>
</html>
''',
        'expected_language': 'html',
        'filename': 'dashboard.html'
    },
    
    'dart_basic': {
        'code': '''
void main() {
    print('Hello, Dart!');
    
    var name = 'Dart';
    String message = 'Welcome to Dart programming';
    int number = 42;
    List<String> languages = ['Dart', 'Flutter'];
    
    var user = User('John', 25);
    user.displayInfo();
}

class User {
    final String name;
    final int age;
    
    User(this.name, this.age);
    
    void displayInfo() {
        print('Name: $name, Age: $age');
    }
}

abstract class Animal {
    void makeSound();
}

class Dog extends Animal {
    @override
    void makeSound() {
        print('Woof!');
    }
}
''',
        'expected_language': 'dart',
        'filename': 'main.dart'
    },
    
    'flutter_basic': {
        'code': '''
import 'package:flutter/material.dart';

void main() {
    runApp(MyApp());
}

class MyApp extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            title: 'Flutter Demo',
            theme: ThemeData(
                primarySwatch: Colors.blue,
            ),
            home: HomePage(title: 'Flutter Demo Home Page'),
        );
    }
}

class HomePage extends StatefulWidget {
    HomePage({Key? key, required this.title}) : super(key: key);
    
    final String title;
    
    @override
    _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
    int _counter = 0;
    
    void _incrementCounter() {
        setState(() {
            _counter++;
        });
    }
    
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text(widget.title),
            ),
            body: Center(
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                        Text('You have pushed the button this many times:'),
                        Text(
                            '$_counter',
                            style: Theme.of(context).textTheme.headlineMedium,
                        ),
                    ],
                ),
            ),
            floatingActionButton: FloatingActionButton(
                onPressed: _incrementCounter,
                tooltip: 'Increment',
                child: Icon(Icons.add),
            ),
        );
    }
}
''',
        'expected_language': 'dart',
        'expected_framework': 'flutter',
        'filename': 'main.dart'
    }
}


def get_test_sample(name: str) -> dict:
    """Get a specific test sample by name"""
    return TEST_SAMPLES.get(name)


def get_all_test_samples() -> dict:
    """Get all test samples"""
    return TEST_SAMPLES


def get_samples_by_language(language: str) -> dict:
    """Get all samples for a specific language"""
    return {
        name: sample for name, sample in TEST_SAMPLES.items()
        if sample['expected_language'] == language
    }


if __name__ == "__main__":
    # Quick test of samples
    print("Available test samples:")
    for name, sample in TEST_SAMPLES.items():
        framework = f" ({sample.get('expected_framework', 'no framework')})" 
        print(f"  {name}: {sample['expected_language']}{framework}")
