<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>Vue博客</h3>
        <p>一个基于Vue.js和Django的现代化博客系统，分享技术，记录生活。</p>
      </div>
      
      <div class="footer-section">
        <h4>快速链接</h4>
        <ul class="footer-links">
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/posts">文章列表</router-link></li>
          <li><router-link to="/about">关于我们</router-link></li>
          <li><router-link to="/contact">联系我们</router-link></li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>技术栈</h4>
        <ul class="tech-list">
          <li>Vue.js 3</li>
          <li>Django 5.2</li>
          <li>Pinia</li>
          <li>SQLite</li>
        </ul>
      </div>
      
      <div class="footer-section">
        <h4>联系方式</h4>
        <div class="contact-info">
          <p>📧 contact@vueblog.com</p>
          <p>🌱 学习项目，仅供演示</p>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <p>&copy; 2024 Vue博客. 保留所有权利.</p>
      <p>用 ❤️ 和 ☕ 制作</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background-color: #2c3e50;
  color: white;
  padding: 3rem 0 1rem;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h3 {
  color: #42b983;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.footer-section h4 {
  color: #42b983;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.footer-section p {
  line-height: 1.6;
  color: #bdc3c7;
  margin-bottom: 0;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.5rem;
}

.footer-links a {
  color: #bdc3c7;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #42b983;
}

.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-list li {
  color: #bdc3c7;
  margin-bottom: 0.5rem;
  padding-left: 1rem;
  position: relative;
}

.tech-list li::before {
  content: "▸";
  position: absolute;
  left: 0;
  color: #42b983;
}

.contact-info p {
  margin-bottom: 0.5rem;
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1.5rem 20px 0;
  border-top: 1px solid #34495e;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-bottom p {
  margin: 0;
  color: #95a5a6;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .footer {
    padding: 2rem 0 1rem;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>