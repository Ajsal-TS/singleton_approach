Your code: obj = ObjWithoutSingleton(1,2,3)  ← args=(1,2,3)

↓

type.__call__(ObjWithoutSingleton, (1,2,3))  ← Metaclass-level call

↓ Internal:

  ObjWithoutSingleton.__new__(ObjWithoutSingleton, (1,2,3))  ← Creates blank obj
  │
  └─ Returns new_instance

↓

ObjWithoutSingleton.__init__(new_instance, (1,2,3))  ← Sets self.args=(1,2,3), logs "Initialized..."

↓

Return new_instance  ← obj points to it



Your code: s = Obj(1,2,3)  ← First time

↓

SingletonMeta.__call__(Obj, (1,2,3))  ← Intercepted at metaclass

↓ Check: Obj not in _instances?

  Yes → with lock: super().__call__(Obj, (1,2,3))  ← Delegates to NORMAL flow
         │
         ↓ Internal (normal):
           Obj.__new__(Obj, (1,2,3))  ← super(Obj, type).__new__ (blank instance)
           │
           └─ instance = new blank
         ↓
           Obj.__init__(instance, (1,2,3))  ← Sets self.args=(1,2,3), logs "Initialized..."
         ↓
         Store instance in _instances[Obj]
         Log INFO "Created new..."

↓ Return instance  ← s points to it

---

Later: d = Obj(4,5,6)

↓ SingletonMeta.__call__(Obj, (4,5,6))

↓ Check: Obj in _instances? Yes → Log DEBUG "Returning existing..."

↓ Return _instances[Obj]  ← d points to SAME instance (ignores (4,5,6))