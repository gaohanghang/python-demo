# 使用Flasgger让Python具有Swagger接口文档功能(翻译)

> 原作者: Bruno Rocha
>
> 原文地址: [Flasgger - API playground with Flask and Swagger UI]([http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html](http://brunorocha.org/python/flask/flasgger-api-playground-with-flask-and-swagger-ui.html))
>
> 翻译: 高行行
>
> 代码地址: 

# Swagger是什么？

Swagger是RESTful API简单而强大的代表。凭借全球最大的API工具生态系统和数千名开发人员。几乎所有现代编程语言和部署环境中都支持Swagger。使用支持 Swagger 的API，您可以获得交互式文档，客户端SDK生成和可见性。

# Swagger UI是什么?

Swagger UI是一个HTML，Javascript和CSS无依赖关系集合，可以从符合Swagger规范的API动态生成漂亮的文档和沙箱。由于Swagger UI没有依赖关系，因此你可以在任何服务器环境或本地计算机上托管它。跳转到[Swagger UI 在线演示](http://petstore.swagger.io/)

# Flask什么? 

Flask是基于Werkzeug，Jinja 2的Python微框架。为什么它非常棒？因为它简单但功能强大，沟通代码更方便！

```python
from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('my_awesome_api', methods=['POST'])
def my_awesome_endpoint():
    data = request.json
    return jsonify(data=data, meta={"status": "ok"})

app.run()
```

运行上面的脚本，然后就可以开始发送请求到API

```shell
curl -XPOST http://localhost:5000/my_awesome_api -d '{"python": "is awesome"}'
{
    "data": {"python": "is awesome"},
    "meta": {"status": "ok"}
}
```

# Flasgger是什么？

Flasgger是Flask的扩展，用于帮助创建Flask API，其中包含由SwaggerUI提供支持的文档和调试工具。你可以使用YAML文件定义API结构，Flasgger会为你创建所有规范，你可以使用相同的模式来验证数据。

GITHUB REPO: https://github.com/rochacbruno/flasgger

# 安装

```shell
pip install flasgger
```

# 创建应用程序

您可以将API规范直接放在 docstrings 中

```python
import random
from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

@app.route('/api/<string:language>/', methods=['GET'])
def index(language):
    """
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic", 
        "simple", "powerful", "amazing", 
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


app.run(debug=True)
```

# 运行

现在运行应用程序并访问 [http://localhost:5000/apidocs/index.html](http://localhost:5000/apidocs/index.html) 将会跳转到 Swagger UI 界面

**启动效果**

![](https://raw.githubusercontent.com/gaohanghang/images/master/img20190907195235.png)

**Swagger 测试效果**

![](https://raw.githubusercontent.com/gaohanghang/images/master/img20190907194745.png)

> 注意: 可以在配置中更改所有默认URL。

**也可以使用单独的文件进行规范**

# 在单独的YML文件中创建api规范

在文件中`index.yml`放入specs定义

```yaml
    This is the language awesomeness API
    Call this api passing a language name and get back its features
    ---
    tags:
      - Awesomeness Language API
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]
```

更改代码，使用 `swag_from` 注解从文件中读取API规范

```python
import random
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
Swagger(app)

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from('index.yml')
def index(language):
    language = language.lower().strip()
    features = [
        "awesome", "great", "dynamic", 
        "simple", "powerful", "amazing", 
        "perfect", "beauty", "lovely"
    ]
    size = int(request.args.get('size', 1))
    if language in ['php', 'vb', 'visualbasic', 'actionscript']:
        return "An error occurred, invalid language for awesomeness", 500
    return jsonify(
        language=language,
        features=random.sample(features, size)
    )


app.run(debug=True)
```

**运行效果**

![](https://raw.githubusercontent.com/gaohanghang/images/master/img20190907200817.png)

# 验证

如果将规范放在单独的文件中，也可以使用相同的规范来验证输入

```python
from flasgger.utils import swag_from, validate, ValidationError

@app.route('/api/<string:language>/', methods=['GET'])
@swag_from('index.yml')
def index(language):
    ...
    try:
        validate(data, 'awesome', 'index.yml', root=__file__)
    except ValidationError as e:
        return "Validation Error: %s" % e, 400
    ...
```

# 更多信息

你可以在flasgger官方github仓库中找到更多信息和一些[示例](https://github.com/rochacbruno/flasgger/blob/master/flasgger/example_app.py) 在这个 [github 仓库](https://github.com/rochacbruno/flasgger/)