import pytest
import optimizer
import itertools

@pytest.fixture()
def setup_optimizer():
    opt = optimizer.Optimizer(1, 10)
    yield opt
def test_add_interval_start(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', start=2)
    opt.add_interval('B', start=3)
    opt.add_interval('C', start=4)
    opt.solve()
    assert [2, 3, 4] == [x.varValue for x in opt.C][::2]
def test_add_interval_end(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', end=2)
    opt.add_interval('B', end=3)
    opt.add_interval('C', end=4)
    opt.solve()
    assert [2, 3, 4] == [x.varValue for x in opt.C][1::2]
def test_add_interval_length(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A', length=2)
    opt.add_interval('B', length=3)
    opt.add_interval('C', length=4)
    opt.solve()
    assert [2, 3, 4] == [(opt.C[i + 1].varValue - opt.C[i].varValue) for i in range(0, len(opt.C), 2)]
def test_interval_overlap(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval('A')
    opt.add_interval('B')
    opt.add_interval('C')
    opt.add_interval_overlap('A', 'B', 2)
    opt.add_interval_overlap('A', 'C', 3)
    opt.add_interval_overlap('B', 'C', 4)
    opt.solve()
    assert [2, 3, 4] == [((a & b).upper - (a & b).lower) for a, b in list(itertools.combinations(opt.as_intervals(), 2))]
def test_interval_order(setup_optimizer):
    opt = setup_optimizer
    with pytest.raises(TypeError):
        opt.add_interval_order('A', 'B', 2)

    opt.add_interval('A')
    opt.add_interval('B')
    opt.add_interval('C')
    opt.add_interval_order('A', 'B', 2)
    opt.add_interval_order('B', 'C', 3, starts=True)
    opt.solve()
    assert 2 == opt.C[2] - opt.C[1]
    assert 3 == opt.C[4] - opt.C[2]