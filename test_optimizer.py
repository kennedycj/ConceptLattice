import pytest
import optimizer

@pytest.fixture()
def setup_optimizer():
    opt = optimizer.Optimizer(3, 1, 10)
    yield opt
def test_interval_start_constraint(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval_start_constraint('A', 2)
    opt.add_interval_start_constraint('B', 3)
    opt.add_interval_start_constraint('C', 4)
    opt.solve()
    assert [x.varValue for x in opt.C][::2] == [2, 3, 4]

def test_interval_end_constraint(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval_end_constraint('A', 2)
    opt.add_interval_end_constraint('B', 3)
    opt.add_interval_end_constraint('C', 4)
    opt.solve()
    assert [x.varValue for x in opt.C][1::2] == [2, 3, 4]

def test_interval_length_constraints(setup_optimizer):
    opt = setup_optimizer
    opt.add_interval_length_constraint('A', 2)
    opt.add_interval_length_constraint('B', 3)
    opt.add_interval_length_constraint('C', 4)
    opt.solve()
    assert [(opt.C[i + 1].varValue - opt.C[i].varValue) for i in range(0, len(opt.C), 2)] == [2, 3, 4]