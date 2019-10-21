# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       26.py
   Description :
   Author :          cugxy
   date：            2019/10/12
-------------------------------------------------
   Change Activity:
                     2019/10/12
-------------------------------------------------

只在使用 Mix-in 组件制作工具类时进行多重继承

- 能够使用 mix-in 组件实现的效果, 就不要用多重继承来做
- 将各功能实现为可插拔的 mix-in 组件, 然后令相关的类继承自己所需要的那些组件, 即可定制该类实例所具备的行为
- 把简单的行为封装到 mix-in 组件里, 然后就可以用多个 mix-in 组合出复杂的行为

"""
import json


class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, val in instance_dict.items():
            output[key] = self._traverse(key, val)
        return output

    def _traverse(self, key, val):
        if isinstance(val, ToDictMixin):
            return val.to_dict()
        elif isinstance(val, dict):
            return self._traverse_dict(val)
        elif isinstance(val, list):
            return [self._traverse(key, e) for e in val]
        elif hasattr(val, '__dict__'):
            return self._traverse_dict(val.__dict__)
        else:
            return val


class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class BinaryTree(ToDictMixin):
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.rigth = right


class BinaryTreeWithParent(BinaryTree):
    def __init__(self, val, left=None, right=None, parent=None):
        super().__init__(val, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, val):
        if isinstance(val, BinaryTreeWithParent) and key == 'parent':
            return val.val
        else:
            return super()._traverse(key, val)


class NamedSubTree(ToDictMixin):
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree = tree_with_parent


class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = switch
        self.machines = [Machine(**kwargs) for kwargs in machines]


class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores=None, ram=None, disk=None):
        self.cores = cores
        self.ram = ram
        self.disk = disk


class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports=None, speed=None):
        self.ports = ports
        self.speed = speed


if __name__ == '__main__':
    if 1:
        tree = BinaryTree(10, left=BinaryTree(7, right=BinaryTree(9)), right=BinaryTree(14, left=BinaryTree(11)))
        print(tree.to_dict())
    if 1:
        root = BinaryTreeWithParent(10)
        root.left = BinaryTreeWithParent(7, parent=root)
        root.left.rigth = BinaryTreeWithParent(9, parent=root.left)
        print(root.to_dict())
        xy_tree = NamedSubTree('xyz', root.left)
        print(xy_tree.to_dict())
    if 1:
        serialized = """{
            "switch": {"ports": 5, "speed": 1e9},
            "machines": [
                {"cores": 8, "ram": 32e9, "disk": 5e12},
                {"cores": 4, "ram": 16e9, "disk": 1e12},
                {"cores": 2, "ram": 4e9, "disk": 500e9}
            ]
        }
        """
        deserialized = DatacenterRack.from_json(serialized)
        roundtrip = deserialized.to_json()
        print(roundtrip)
        assert json.loads(serialized) == json.loads(roundtrip)
    pass



