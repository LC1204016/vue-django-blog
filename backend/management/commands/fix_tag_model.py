from django.core.management.base import BaseCommand
from django.db import connection
from backend.models import Category, Tag, CategoryTag


class Command(BaseCommand):
    help = '修复Tag模型并创建分类标签关联'

    def handle(self, *args, **options):
        # 直接使用SQL修复Tag表结构
        with connection.cursor() as cursor:
            # 检查是否存在错误的category_id字段
            cursor.execute("""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'backend_tag' 
                AND COLUMN_NAME = 'category_id'
            """)
            has_category_id = cursor.fetchone()[0]
            
            if has_category_id:
                cursor.execute("ALTER TABLE backend_tag DROP COLUMN category_id")
                self.stdout.write(self.style.SUCCESS('已删除Tag表中的错误category_id字段'))
            else:
                self.stdout.write('Tag表结构正常，无需修复')
        
        # 重新创建分类和标签关联
        self.stdout.write('\n开始创建分类和标签关联关系...')
        
        # 清理现有的关联关系
        CategoryTag.objects.all().delete()
        self.stdout.write('已清理现有的分类-标签关联关系')

        # 创建分类
        categories_data = [
            {'name': '技术', 'description': '技术相关文章'},
            {'name': '生活', 'description': '日常生活分享'},
            {'name': '学习', 'description': '学习笔记和心得'},
            {'name': '娱乐', 'description': '娱乐和休闲内容'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                category=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'成功创建分类: {category.category}'))
            else:
                self.stdout.write(f'分类已存在: {category.category}')

        # 创建标签
        tags_data = [
            'Python', 'Django', 'Vue.js', 'JavaScript', '前端', '后端',
            '数据库', '算法', '设计', '摄影', '旅行', '美食',
            '读书', '电影', '音乐', '游戏', '运动', '健康'
        ]

        for tag_name in tags_data:
            try:
                tag = Tag.objects.get(tag=tag_name)
                self.stdout.write(f'标签已存在: {tag.tag}')
            except Tag.DoesNotExist:
                tag = Tag.objects.create(tag=tag_name)
                self.stdout.write(self.style.SUCCESS(f'成功创建标签: {tag.tag}'))

        # 建立分类和标签的关联关系
        category_tag_relations = {
            '技术': ['Python', 'Django', 'Vue.js', 'JavaScript', '前端', '后端', '数据库', '算法'],
            '生活': ['摄影', '旅行', '美食', '运动', '健康'],
            '学习': ['Python', 'Django', 'Vue.js', 'JavaScript', '读书', '算法'],
            '娱乐': ['电影', '音乐', '游戏', '旅行', '摄影'],
        }

        for category_name, tag_names in category_tag_relations.items():
            try:
                category = Category.objects.get(category=category_name)
                for tag_name in tag_names:
                    try:
                        tag = Tag.objects.get(tag=tag_name)
                        category_tag = CategoryTag.objects.create(
                            category=category,
                            tag=tag
                        )
                        self.stdout.write(self.style.SUCCESS(f'成功创建关联: {category.category} - {tag.tag}'))
                    except Tag.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'标签不存在: {tag_name}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'分类不存在: {category_name}'))

        self.stdout.write(self.style.SUCCESS('分类和标签关联关系创建完成！'))

        # 显示统计信息
        self.stdout.write('\n统计信息:')
        self.stdout.write(f'分类总数: {Category.objects.count()}')
        self.stdout.write(f'标签总数: {Tag.objects.count()}')
        self.stdout.write(f'关联关系总数: {CategoryTag.objects.count()}')

        # 显示每个分类的标签
        self.stdout.write('\n分类标签详情:')
        for category in Category.objects.all():
            tags = [ct.tag.tag for ct in category.category_tags.all()]
            self.stdout.write(f'{category.category}: {", ".join(tags)}')
            
        # 测试Category模型的便捷方法
        self.stdout.write('\n测试Category模型的便捷方法:')
        tech_category = Category.objects.get(category='技术')
        self.stdout.write(f'技术分类的标签: {[tag.tag for tag in tech_category.tags]}')
        
        # 测试添加新标签
        new_tag = tech_category.add_tag('测试标签')
        self.stdout.write(f'添加新标签到技术分类: {new_tag.tag}')
        self.stdout.write(f'技术分类的新标签列表: {[tag.tag for tag in tech_category.tags]}')
        
        # 测试移除标签
        success = tech_category.remove_tag('测试标签')
        self.stdout.write(f'从技术分类移除测试标签: {"成功" if success else "失败"}')
        self.stdout.write(f'技术分类的最终标签列表: {[tag.tag for tag in tech_category.tags]}')