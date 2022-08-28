from python.try1.try5._try5 import Arc


def insertBefore(x: Arc, y: Arc):
    if x.left is None:
        x.left = y
        y.parent = x
    else:
        x.prev.right = y
        y.parent = x.parent
    y.prev = x.prev
    if y.prev is not None:
        y.prev.next = y

    y.next = x
    x.prev = y

    insertFixup(y)


def insertFixup(y: Arc):
    raise NotImplementedError()


def insertAfter(x: Arc, y: Arc):
    raise NotImplementedError()

