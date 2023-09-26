import pytest
import optimizer

@pytest.fixture()
def setup_optimizer():
    opt = optimizer.Optimizer(3, 1, 10)
    yield opt
def test_add_interval_start(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', start=2)
    opt.add_interval('B', start=3)
    opt.add_interval('C', start=4)
    opt.solve()
    assert [x.varValue for x in opt.C][::2] == [2, 3, 4]
def test_add_interval_end(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', end=2)
    opt.add_interval('B', end=3)
    opt.add_interval('C', end=4)
    opt.solve()
    assert [x.varValue for x in opt.C][1::2] == [2, 3, 4]
def test_add_interval_length(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', length=2)
    opt.add_interval('B', length=3)
    opt.add_interval('C', length=4)
    opt.solve()
    assert [(opt.C[i + 1].varValue - opt.C[i].varValue) for i in range(0, len(opt.C), 2)] == [2, 3, 4]