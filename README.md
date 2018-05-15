# Bors
A highly flexible and extensible service integration framework for scraping the web or consuming APIs.

# Usage
1. Create your model based on the data you expect to incorporate.
2. Decide on what you want to do with your data, and add it.
3. Create or use an existing API integration library.
4. Create your root application to tie it all together.

## Object Model
We use [marshmallow](https://marshmallow.readthedocs.io/en/latest/) for the underlying object schema definitions.  Here's an example model:

```python
from marshmallow import Schema, fields

class NewsItemSchema(Schema):
    """News item"""
    id = f.Str(required=True)
    url = f.Str(required=True)
    title = f.Str(required=True)
    pubDate = f.Str(required=True)
    timestamp = f.Str(required=True)
    feed_id = f.Int(required=True)
    published_date = f.Str(required=True)
    feed_name = f.Str(required=True)
    feed_url = f.Str(required=True)
    feed_enabled = f.Int(required=True)
    feed_description = f.Str(required=True)
    url_field = f.Str(required=True)
    title_field = f.Str(required=True)
    date_field = f.Str(required=True)
    feed_image = f.Str(required=True)
```
See the `marshmallow` docs for more information.

## Middleware Strategies
Middleware API is implemented in the form of strategies and follows this basic layout:
```python
"""
Simple context display strategy
"""

from bors.app.strategy import IStrategy


class Print(IStrategy):
    """Print Strategy implementation"""
    def bind(self, context):
        """
        Bind the strategy to the middleware pipeline,
        returning the context
        """
        print(f"""PrintStrategy: {context}""")

        # just a pass-through
        return context
```
The important things to note here:
* We're inheriting from `IStrategy`.
* We're implementing a `bind` method.
* The bind method receives, potentially augments, and then returns the `context`.

## API Integration

### Request Schema

Because our API is simple, we're going to use this as-is.

```python
from bors.generics.request import RequestSchema
```

### Response Schema

Our API sends us data in the following format:
```json
{
    "data": ...,
    "status": "OK"
}
```

For this, we'll need to supplement a bit, removing the root fields and returning the `data` value:
```python
from marshmallow import fields
from bors.generics.request import ResponseSchema


class MyAPIResponseSchema(ResponseSchema):
    """Schema defining how the API will respond"""
    status = fields.Str()
    def get_result(self, data):
        """Return the actual result data"""
        return data.get("data", "")
        
    class Meta:
        """Add 'data' field"""
        strict = True
        additional = ("data",)
```

### API Class

```python
from bors.api.requestor import Req


class MyAPI(LoggerMixin):
    name = "my_api"
    def __init__(self, context):
        self.create_logger()
        
        self.request_schema = RequestSchema
        self.result_schema = MyAPIResponseSchema
        self.context = context
        
        self.req = Req("http://some.api.endpoint/v1", payload, self.log)
        
        # We don't need to deal directly with requests, so we pass them through
        self.call = self.req.call
    
    def shutdown(self):
        """Perform last-minute stuff"""
        pass
```
Here we use the built-in `Req` class to issue requests to the API, we assign the `request_schema` and `result_schema` to classes in our object, and we set the `name`, `context`, and `call` attributes.  The results passed through on the API are referencable from within the middleware context under the key `my_api`.

### Pulling it all together

```python
from bors.app.builder import AppBuilder
from bors.app.strategy import Strategy


def main():
    strat = Strategy(Print())
    app = AppBuilder([MyAPI], strat)
    app.run()
    
if __name__ == "__main__":
    main()
```
Here, we set as many strategies and API's as we want, then create and run the `app`.

# Architecture
      +------------+
    +-+ MIDDLEWARE +------> out
    | +------------+
    |                       API/WEB
    | +------------+
    +-+ PREPROCESS +<------ in
      +------------+

At its most basic level, a `bors` integrator engages with an integration library (API) passing incoming data through a prepocessor to generate and validate incoming objects, then passes that data through middlewares.  Outgoing interactions are initiated from within a middleware and passed directly to an API, allowing easily for request/response type behavior in addition to observe and react.

### Ingesting Data

          ^
          |
    +-----+------+
    | MIDDLEWARE |
    +-----+------+
          ^
    +-----+------+
    | PREPROCESS |
    +-----+------+
          ^
          |
          +
         API/
         WEB

Ingested data provokes calls along the pipeline.

### Outgoing Data
         API/
         WEB
          ^
          |
    +-----+------+
    | MIDDLEWARE |
    +------------+
Enacted events stimulate API or web actions.

## Preprocessing
Preprocessing is nothing more than an object-ization of the incoming data.  This provides two benefits:
1. Data can be generalized across API interfaces.
2. Data structure can be validated and enforced.

## Middlewares

Middlewares allow for a data processing pipeline to pass data through.

      +-+  +-+  +-+
      |M|  |M|  |M|
      |I|  |I|  |I|
      |D|  |D|  |D|
      |D|  |D|  |D|
    ->+L+->+L+->+L+->
      |E|  |E|  |E|
      |W|  |W|  |W|
      |A|  |A|  |A|
      |R|  |R|  |R|
      |E|  |E|  |E|
      +-+  +-+  +-+


With this model, we gain a lot of flexibility in the behavior of our integration.  Middleware is up to the developer to create, and can be any of the following:

* Data post-processing, filtering, aggregation, or augmentation
* External integrations and interfaces
* Stimulate an API/web transaction from external actors or time-based criteria
* Hooks and callbacks
