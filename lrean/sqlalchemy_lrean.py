import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import aliased


print('sqlalchemy.__version__ : %s' % sqlalchemy.__version__)
engine = create_engine('sqlite:///test.db', echo=True)   # echo 表示 是否启动日志 此时并不会真正与数据库建立连接
Base = declarative_base()   # 我们的 表对象继承与此

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"useexisting": True}
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name=%s, fullname='%s')>" % (self.name, self.fullname, )

print('User.__table__: %s ' % User.__table__)
print('create_all() : %s ' % Base.metadata.create_all(engine))

xy_user = User(name='xy', fullname='cugxy', password='123')

print('xy_user.name: %s' % xy_user.name)
print('xy_user.id: %s' % str(xy_user.id))

Session = sessionmaker(bind=engine)     # 创建 数据库 session  还可以  Session = sessionmaker() Session.configure(bind=engine)  
session = Session() 
# 上面的Session是和我们的SQLite-enabled引擎相关联的，                  
# 但是现在还没有与数据库链接。当他第一次被调用的时候才会建立与一个Engine维护的连接池连接，一直持续到我们关闭Session对象，或者提交完所有的变化。

# 会话的生命周期模式（Session Lifecycle Patterns）说明时候创建一个会话依赖于我们在创建一个说明应用。
# 记住，对话只是你对象指向一个数据库链接的一个工作空间，如果把对象进程比作一个晚宴，那么来宾的盘子还有盘子上的食物则是回话（数据库就是厨房？）

# （Adding and Updating Objects）
# session.add(xy_user)

# 现在，我们称这个对象是待定的（pending）；现在没有任何SQL语句被执行，同时这个对象也并代表数据库中的一行数据。
# 对话（Session）会在需要的时候尽快持久化，这个过程称之为 flush 。
# 如果我们在数据库里查询，所有的待定信息（pending information）都会首先被flush（冲刷？），随机查询请求被执行。

our_user = session.query(User).filter_by(name='xy').first()
print('our_user: %s' % our_user)

# ORM的概念在工作的地方会识别并且保证会是在一个特殊的行上。一旦一个对象已经在会话中有一个主键（primary key），
# 所有关于这个key的SQL查询都只返回一个同样的Python对象，如果已经存在某个主键的对象，此时想添加一个同样主键的对象，就会引起一个错误。

# session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'), 
#     User(name='mary', fullname='Mary Contrary', password='xxg527'),
#     User(name='fred', fullname='Fred Flinstone', password='blah')])
print('session.new:%s' % session.new)

xy_user.password = '123456'
print('session.dirty:%s' % session.dirty)

session.commit()

print('session.new:%s' % session.new)
print('session.dirty:%s' % session.dirty)

# 既然会话在一个事务里边起作用，那么我们也可以在这个事务里回滚一些变化。
xy_user.fullname = 'xixixi'
fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)
print(session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())
session.rollback()
print('xy_user.fullname : %s' % xy_user.fullname)
print('fake_user in session :%r' % (fake_user in session))

# Query返回的结果称之为元组（tuples），通过KeyedTupleclass实现，同时可以被当做Python的原生对象来处理。
# 参数的名称和参数一样，类名和类一样
# （不知道咋翻译，原文： The names are the same as the attribute’s name for an attribute, and the class name for a class，
# 看例子理解的意思就是：row对应的是User, 想获取name就使用row.name，这样row和row.name分别都有其对应的User，User.name了）
print('query User---------------------------------------------------')
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)
print('query User, User.name---------------------------------------------------')
for row in session.query(User, User.name).all():
    print(row.name)
# 可以使用类元素衍生的一个对象lable()构造（construct）来给一列起另外的称呼，任何一个类的参数都可以这样使用（功能就像名字一样，打标签，起别名）：
print('query User.name as name_label---------------------------------------------------')
for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)
print('query user_alias, user_alias.name---------------------------------------------------')
user_alias = aliased(User, name='user_alias')
for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias, row.name)

# 过滤结果使用filter_by()来实现，使用的参数是关键字：
# 或者使用filter()，filter()使用更灵活的SQL语句的结构来过滤。这可以让你使用规律的Python操作符来操作你映射的类参数：

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)
for name, in session.query(User.name).filter(User.fullname=='Ed Jones'):
    print(name)
# 常用过滤操作（Common Filter Operators）
# 这里是一份常用过滤操作的摘要：

# EQUALS
session.query(User).filter(User.name == 'ed')

# NOT EQUALS
session.query(User).filter(User.name != 'ed')

# LIKE
session.query(User).filter(User.name.like('%ed%'))

# IN
session.query(User).filter(User.name.in_(['ed', 'wendy', 'jack']))
# works with query objects too:
session.query(User).filter(User.name.in_(session.query(User.name).filter(User.name.like('%ed%')) ))

# NOT IN
session.query(User).filter(~User.name.in_(['ed', 'wendy', 'jack']))

# IS NULL
session.query(User).filter(User.name == None)
# alternatively, if pep8/linters are a concern
session.query(User).filter(User.name.is_(None))

# IS NOT NULL
session.query(User).filter(User.name != None)
# alternatively, if pep8/linters are a concern
session.query(User).filter(User.name.isnot(None))

# AND
# use and_()
from sqlalchemy import and_
session.query(User).filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
# or send multiple expressions to .filter()
session.query(User).filter(User.name == 'ed', User.fullname == 'Ed Jones')
# or chain multiple filter()/filter_by() calls
session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
# 注意 是 and_() 不是Python里的and操作符

# OR
from sqlalchemy import or_
session.query(User).filter(or_(User.name == 'ed', User.name == 'wendy'))
# 注意 是 or_() 不是Python里的or操作符

# MATCH
session.query(User).filter(User.name.match('wendy'))
# 注意 match() 使用MATCH 或者 CONTAINS 来实现的，所以和数据库底层有关，在一些数据库下不能使用，比如说SQLite

# 查询返回的列表以及标量（Returning Lists and Scalars）

# all()
session.query(User).all()

# first() 对查询结果进行了一个限制-返回列表的第一个值：
session.query(User).first()

# one()完全匹配所以行，如果匹配不到，则返回一个错误，或者匹配到多个值也会返回错误：
session.query(User).one()

# one()对于那些希望分别处理查询不到与查询到多个值的系统是十分好的，比方说在RESTful API中，查询不到可能会返回404页面，多个结果则可能希望返回一个应用错误。
# one_or_none()和one()很像，除了在查询不到的时候。查询不到的时候one_or_none()会直接返回None，但是在找到多个值的时候和one()一样。
session.query(User).one_or_none()
# scalar()援引自one()函数，查询成功之后会返回这一行的第一列参数，如下：

query_result = session.query(User.id).filter(User.name == 'xy').order_by(User.id)
query_result.scalar()

# 使用SQL语句查询（Using Textual SQL）
from sqlalchemy import text
for user in session.query(User).filter(text('id<224')).order_by(text('id')).all():
    print(user.name)

# 使用基于字符串的SQL语句（string-based SQL）可以通过冒号来指定参数。为参数复制可以使用params()来实现：
session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(User.id).one()

# 为了使用完全基于字符串的语句，可以使用from_statement()来实现。不需要额外的指定，完全的字符串SQL语句是根据模型（model）的名字来匹配的，
# 如下，我们仅使用了一个星号就获取到了所有的信息（查找名字为ed的行）
session.query(User).from_statement(text("SELECT * FROM users where name=:name")).params(name='ed').all()

# 除此之外，有一个典型的表现就是在我们匹配结果的时候，我们可能会发现处理找到的结果也是十分有必要的。
# 在这种情况下，text()架构允许我们把纯SQL语句与ORM映射对应起来，我们通过TextClause.columns()方法可以传一些表达式参数：
stmt = text("SELECT name, id FROM users where name=:name")
stmt = stmt.columns(User.name, User.id)
session.query(User.id, User.name).from_statement(stmt).params(name='ed').all()

# count()
from sqlalchemy import func
session.query(func.count(User.name), User.name).group_by(User.name).all()
# 或者
session.query(User).count()
