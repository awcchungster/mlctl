from kfp import dsl


def pipeline(function):

    print('decorating', function)
    # def wrapper():

    #     function()
    
    # return wrapper
    # 
    # response = f()
    # return response

    @dsl.pipeline(name='kfp_test',description='kfp_description')
    def wrapper(name=None, description=None):
        function()
        return
    return wrapper
