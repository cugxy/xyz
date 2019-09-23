# Celery

## 配置
### 基础配置
```python
class Config:
    """
    配置类
    """

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = os.environ.get('CACHE_REDIS_HOST') or '127.0.0.1'
    CACHE_REDIS_PORT = os.environ.get('CACHE_REDIS_PORT') or 6379
    CACHE_REDIS_DB = os.environ.get('CACHE_REDIS_DB') or '1'
    CACHE_REDIS_PASSWORD = os.environ.get('CACHE_REDIS_PASSWORD') or 'greenvalley'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 'redis://auth:password@redishost:6379/0'
    CELERY_BROKER_URL = 'redis://auth:%s@%s:%s/10' % (CACHE_REDIS_PASSWORD, CACHE_REDIS_HOST, CACHE_REDIS_PORT, )
    CELERY_RESULT_BACKEND = 'redis://auth:%s@%s:%s/11' % (CACHE_REDIS_PASSWORD, CACHE_REDIS_HOST, CACHE_REDIS_PORT, )
    CELERY_DISABLE_RATE_LIMITS = True

    @staticmethod
    def init_app(app):
        pass
```

## task
### 基本用法

```python
@app.task
def add(a, b):
    return a + b
```
- 当使用多个 解释器 在任务函数上时, 请确保 `task` 解释器在最外面.

### 名称
每个任务将会有一个独一无二的名称, 如果用户未指定名称, celery 会自动生成一个
```python
@app.task(name='sum-of-two-numbers')
def add(a, b):
    return a + b
```
- 最好的名称是模块名称
```python
@app.task(name='tasks.add')
def add(a, b):
    return a + b
```
- 当使用相对导入时, 自动生成名称可能抛出 `NotRegistered` 异常

### content

### 日志
```python
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task
def add(x, y):
    logger.info('Adding {0} + {1}'.format(x, y))
    return x + y
```

### 重试

### 选项列表
可在 `task` 解释器中添加这些选项
- name 名称
- request
- abstract 
- max_retries 最大重试次数, 
- throws 指定可能的 Exception, 此列表中的错误将被报告为结果后端失败，但是工作进程不会将事件记录为错误，并且不会包含任何追溯。
- default_retry_delay
- rate_limit 
- time_limit 任务限时, 如未设置, 将使用 worker 的限时
- soft_time_limit 
- ignore_result 不存储任务状态, 意味着你无法使用 `AsyncResult` 取检查任务是否完成, 或获取任务的返回结果.
- store_errors_even_if_ignored 如果设置未 True, 就算任务被设置了 ignore_result 你还是可以获取到 error
- serializer 默认序列化方法, `json`, `yaml`, 默认为 `CELERY_TASK_SERIALIZER`
- compression 压缩方案, 默认为 `CELERY_MESSAGE_COMPRESSION`, 可用 `gzip` `bzip2`
- backend 结果存储链接, 默认为 `CELERY_RESULT_BACKEND`
- track_started 如果为True，则当 worker 执行任务时，任务将报告其状态为 `started`。

### 状态

Celery可以跟踪任务的当前状态。 状态还包含成功任务的结果，或失败任务的异常和回溯信息。
还有一些状态集，例如FAILURE_STATES集和READY_STATES集。
您还可以定义自定义状态。

- PENDING 任务正在等待执行或未知。 任何未知的任务ID都暗示处于挂起状态。
- STARTED 任务已启动。 默认情况下未报告，要启用，请参阅celery.Task.track_started。 元数据：执行任务的辅助进程的pid和主机名。
- SUCCESS 任务已成功执行。元数据：结果包含任务的返回值。
- FAILURE 任务执行导致失败。元数据：result包含发生的异常，traceback包含引发异常时堆栈的回溯。
- RETRY 任务正在重试。元数据：result包含导致重试的异常，traceback包含引发异常时堆栈的回溯。
- REVOKED 任务已被撤消。
- 自定义状态
    - 您可以轻松定义自己的状态，只需要一个唯一的名称即可。 状态名称通常是大写字符串。 例如，您可以看看定义了自己的自定义ABORTED状态的可中止任务。
    ```python
    @app.task(bind=True)
    def upload_files(self, filenames):
        for i, file in enumerate(filenames):
            self.update_state(state='PROGRESS', meta={'current': i, 'total': len(filenames)})
    ```

### 结果后端

RabbitMQ结果后端（amqp）很特殊，因为它实际上并不存储状态，而是将其作为消息发送。 这是一个重要的区别，因为这意味着结果只能检索一次。 
如果您有两个进程在等待相同的结果，则其中一个进程将永远不会收到结果！即使有此限制，如果您需要实时接收状态更改，它也是一个绝佳的选择。
使用消息传递意味着客户端不必轮询新状态。

### 数据库结果后端 Database Result Backend
对于许多人而言，将状态保存在数据库中可能很方便，特别是对于已经有数据库的Web应用程序，但它也有局限性。

- 轮询数据库以获取新状态非常昂贵，因此您应增加诸如result.get（）之类的操作的轮询间隔。

- 某些数据库使用默认事务隔离级别，该级别不适用于轮询表中的更改。

- 在MySQL中，默认事务隔离级别为REPEATABLE-READ，这意味着在提交事务之前，该事务将看不到其他事务的更改。 建议您更改为READ-COMMITTED隔离级别。

### 自定义任务
所有任务都从celery.Task类继承。 run（）方法成为任务主体。
```python
class _AddTask(app.Task):

    def run(self, x, y):
        return x + y
```

### 回调程序
```
after_return(self, status, retval, task_id, args, kwargs, einfo)
任务结束时回调

参数:	
    status – Current task state.
    retval – Task return value/exception.
    task_id – Unique id of the task.
    args – Original arguments for the task that returned.
    kwargs – Original keyword arguments for the task that returned.
    einfo – ExceptionInfo instance, containing the traceback (if any).
    The return value of this handler is ignored.

on_failure(self, exc, task_id, args, kwargs, einfo)
任务失败时回调

参数:	
    exc – The exception raised by the task.
    task_id – Unique id of the failed task.
    args – Original arguments for the task that failed.
    kwargs – Original keyword arguments for the task that failed.
    einfo – ExceptionInfo instance, containing the traceback.
    The return value of this handler is ignored.

on_retry(self, exc, task_id, args, kwargs, einfo)
任务重试时回调

参数:	
    exc – The exception sent to retry().
    task_id – Unique id of the retried task.
    args – Original arguments for the retried task.
    kwargs – Original keyword arguments for the retried task.
    einfo – ExceptionInfo instance, containing the traceback.
    The return value of this handler is ignored.

on_success(self, retval, task_id, args, kwargs)
任务执行成功后回调

参数:	
    retval – The return value of the task.
    task_id – Unique id of the executed task.
    args – Original arguments for the executed task.
    kwargs – Original keyword arguments for the executed task.
    The return value of this handler is ignored.
```

## 任务调用
### 基础
- `apply_async(args[, kwargs[, ...]])` 发送到任务队列
- `delay(*args, **kwargs)` 发送任务消息的快捷方式，但不支持执行选项。
- calling(__call__) 直接在当前进程调用

### 示例
```python
@app.task
def add(x, y):
    return x + y
    
add.delay(1, 2, kwarg1='x', kwarg2='y')
add.apply_async(args=[1, 2], kwargs={'kwarg1': 'x', 'kwarg2': 'y'})
add.s(1, 2, kwarg1='x', kwargs2='y').apply_async()
```

### 链接（回调/错误回调）
Celery支持将任务链接在一起，以便一个任务紧随另一个任务。 回调任务将与父任务的结果一起用作部分参数
```python
add.apply_async((2, 2), link=add.s(16))

@app.task
def error_handler(uuid):
    result = AsyncResult(uuid)
    exc = result.get(propagate=False)
    print('Task {0} raised exception: {1!r}\n{2!r}'.format( uuid, exc, result.traceback))
          
add.apply_async((2, 2), link_error=error_handler.s())
add.apply_async((2, 2), link=[add.s(16), other_task.s()])
```

### ETA and countdown
通过ETA（预计到达时间），您可以设置特定的日期和时间，这是最早执行任务的时间。 倒数计时是一种以秒为单位设置eta的快捷方式。
```python
result = add.apply_async((2, 2), countdown=3)
result.get()    # this takes at least 3 seconds to return

tomorrow = datetime.utcnow() + timedelta(days=1)
add.apply_async((2, 2), eta=tomorrow)
```

### Expiration
expires参数定义一个可选的到期时间，可以是任务发布后的秒数，也可以使用datetime来指定特定的日期和时间
```
add.apply_async((10, 10), expires=60)
add.apply_async((10, 10), kwargs, expires=datetime.now() + timedelta(days=1)
```

### Message Sending Retry
当连接失败时，Celery会自动重试发送消息，并且可以配置重试行为（例如重试频率或最大重试次数）或一起禁用。
```python
add.apply_async((2, 2), retry=False)

add.apply_async((2, 2), retry=True, retry_policy={
    'max_retries': 3,
    'interval_start': 0,        # Defines the number of seconds (float or integer) to wait between retries. Default is 0, which means the first retry will be instantaneous.
    'interval_step': 0.2,       # On each consecutive retry this number will be added to the retry delay (float or integer). Default is 0.2.
    'interval_max': 0.2,        # Maximum number of seconds (float or integer) to wait between retries. Default is 0.2.
})
```

### Serializers
客户端和 worker 之间传输的数据需要进行序列化，因此Celery中的每条消息都有一个content_type标头，该标头描述了用于对其进行编码的序列化方法。
默认的序列化程序是pickle，但是您可以使用CELERY_TASK_SERIALIZER设置来更改此设置，也可以针对每个单独的任务甚至对每个消息进行更改。
内置了对pickle，JSON，YAML和msgpack的支持，您还可以通过将其注册到Kombu序列化器注册表中来添加自己的自定义序列化器（请参阅ref：kombu：guide-serialization）。
```python
add.apply_async((10, 10), serializer='json')
```

### Compression
Celery可以使用gzip或bzip2压缩消息。 您还可以创建自己的压缩方案并将其注册到kombu压缩注册表中。
Task.compression属性。 CELERY_MESSAGE_COMPRESSION属性。
```python
add.apply_async((2, 2), compression='zlib')
```

## 监控管理指南
### Flower：实时 Celery 网络监视器
- 安装
`pip install flower`
- 启动
`celery flower --broker=redis://auth:greenvalley@192.168.10.156:9025/10`
- 浏览
`http://localhost:5555/dashboard`