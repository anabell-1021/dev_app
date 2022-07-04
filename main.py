from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, static_folder='./static') #(__name__目前執行的模組
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
#app.__static__folder = "./templates/static"

class Todo(db.Model):  #對應DB結構
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])  #以涵式為基礎提供附加功能
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) #新增使用者資料
            db.session.commit()
            return redirect('/')
        except:
            return '新增時有誤'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')  #要處理的網站路徑
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete) #刪除使用者資料
        db.session.commit()
        return redirect('/')
    except:
        return '刪除時有誤'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()  #更新使用者資料
            return redirect('/')
        except:
            return '更新資料有誤'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":  #以主程式執行
    app.run(debug=True)  #立即啟動伺服器