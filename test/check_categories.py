#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from backend.models import Category

# 检查分类数据
print("检查分类数据:")
categories = Category.objects.all()
for cat in categories:
    print(f"ID: {cat.id}, Category: {cat.category}, Type: {type(cat.category)}")
    print(f"  repr(): {repr(cat.category)}")
    print(f"  bytes: {cat.category.encode('utf-8')}")
    print()