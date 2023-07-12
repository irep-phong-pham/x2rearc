#QA: should use Enum or (Class & build-int type)
# Refs: https://medium.com/better-programming/take-advantage-of-the-enum-class-to-implement-enumerations-in-python-1b65b530e1d
class TaskStatus:
    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'
    CLOSE = 'CLOSE'