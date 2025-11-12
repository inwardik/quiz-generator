## Python Advanced Quiz (Senior Level)

#### What is the Global Interpreter Lock (GIL) in Python?

- [ ] A security feature to prevent unauthorized code execution
- [x] A mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously
- [ ] A locking mechanism for file operations
- [ ] A feature that improves multi-threading performance

#### What is the difference between __new__ and __init__?

- [ ] They are the same
- [x] __new__ creates the instance, __init__ initializes it
- [ ] __init__ creates the instance, __new__ initializes it
- [ ] __new__ is for classes, __init__ is for instances

#### What is a metaclass in Python?

- [ ] A base class for all classes
- [ ] An abstract class
- [x] A class of a class that defines how a class behaves
- [ ] A class that cannot be instantiated

#### What does the @property decorator do?

- [ ] Makes a variable private
- [x] Converts a method into a read-only attribute
- [ ] Creates a static method
- [ ] Defines a class variable

#### What is the purpose of the __slots__ attribute?

- [ ] To define method slots
- [x] To restrict instance attributes and reduce memory overhead
- [ ] To create multiple inheritance slots
- [ ] To define private attributes

#### What is the difference between deepcopy and shallow copy?

- [ ] No difference
- [x] Deepcopy recursively copies nested objects, shallow copy doesn't
- [ ] Shallow copy is faster but creates duplicates
- [ ] Deepcopy only works with lists

#### What is a context manager in Python?

- [ ] A memory management tool
- [x] An object that defines __enter__ and __exit__ methods for resource management
- [ ] A module for managing global context
- [ ] A debugging tool

#### What does the yield keyword do?

- [ ] Returns a value and exits the function
- [x] Returns a value and pauses the function, creating a generator
- [ ] Creates an async function
- [ ] Yields control to another thread

#### What is the difference between @staticmethod and @classmethod?

- [ ] No difference
- [x] @classmethod receives the class as first argument, @staticmethod doesn't receive self or cls
- [ ] @staticmethod is faster
- [ ] @classmethod can only be called on instances

#### What are descriptors in Python?

- [ ] Function decorators
- [x] Objects that define __get__, __set__, or __delete__ methods
- [ ] Type hints
- [ ] Documentation strings

#### What is monkey patching?

- [ ] A debugging technique
- [x] Dynamically modifying a class or module at runtime
- [ ] A design pattern
- [ ] A testing framework

#### What does the functools.lru_cache decorator do?

- [ ] Caches all function results permanently
- [x] Implements a Least Recently Used cache for function results
- [ ] Reduces function execution time
- [ ] Logs function calls

#### What is the difference between is and ==?

- [ ] No difference
- [x] is checks identity (same object), == checks equality (same value)
- [ ] is is faster
- [ ] == is deprecated

#### What are Abstract Base Classes (ABC)?

- [ ] Regular base classes
- [x] Classes that define an interface and cannot be instantiated directly
- [ ] Classes with no methods
- [ ] Deprecated feature

#### What is the purpose of __call__ method?

- [ ] To call other methods
- [x] To make an instance callable like a function
- [ ] To initialize the instance
- [ ] To destroy the instance

#### What is a generator expression?

- [ ] A function that generates code
- [x] A memory-efficient way to create iterators using parentheses syntax
- [ ] A list comprehension with generators
- [ ] A pattern matching expression

#### What does the asyncio library provide?

- [ ] Multi-threading support
- [x] Asynchronous I/O and coroutine-based concurrency
- [ ] Parallel processing
- [ ] Distributed computing

#### What is the difference between multiprocessing and threading?

- [ ] No difference
- [x] Multiprocessing uses separate processes (bypasses GIL), threading uses threads within one process
- [ ] Threading is always faster
- [ ] Multiprocessing cannot share data

#### What are coroutines in Python?

- [ ] Regular functions
- [x] Functions that can pause and resume execution using async/await
- [ ] Thread-safe functions
- [ ] Deprecated functions

#### What does the @wraps decorator from functools do?

- [ ] Creates a wrapper class
- [x] Preserves metadata of the wrapped function
- [ ] Improves performance
- [ ] Creates a decorator

#### What is the MRO (Method Resolution Order)?

- [ ] A memory optimization technique
- [x] The order in which Python looks for methods in a hierarchy of classes
- [ ] A method for resolving conflicts
- [ ] A debugging order

#### What is the purpose of __getattr__ and __getattribute__?

- [ ] They are the same
- [x] __getattribute__ is called for every attribute access, __getattr__ only when attribute is not found
- [ ] __getattr__ is faster
- [ ] __getattribute__ is deprecated

#### What are weak references in Python?

- [ ] References to immutable objects
- [x] References that don't prevent garbage collection of the referenced object
- [ ] References with lower priority
- [ ] Deprecated feature

#### What is the purpose of the itertools module?

- [ ] File iteration
- [x] Creating efficient iterators for looping
- [ ] Database iteration
- [ ] Thread iteration

#### What does the collections.namedtuple provide?

- [ ] A dictionary with names
- [x] A tuple subclass with named fields
- [ ] A list with named indexes
- [ ] A set with named elements
