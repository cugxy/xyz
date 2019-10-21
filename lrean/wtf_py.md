## Deep down, we're all the same./本质上,我们都一样. *
` id(WTF()) == id(WTF()) `
` True `
- 因为 id() 函数中，WTF() 对象作用域 为 id 函数，所以刚刚创建便被销毁，然后第二个对象在同一内存空间被创造
