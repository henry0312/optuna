from optuna.study import create_study
from optuna.trial import Trial  # NOQA
from optuna.visualization import _get_intermediate_plot


def test_get_intermediate_plot():
    # type: () -> None

    study = create_study()

    # Test with no trial.
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 0

    def objective(trial, report_intermediate_values):
        # type: (Trial, bool) -> float

        if report_intermediate_values:
            trial.report(1.0, step=0)
            trial.report(2.0, step=1)
        return 0.0

    # Test with a trial with intermediate values.
    study.optimize(lambda t: objective(t, True), n_trials=1)
    figure = _get_intermediate_plot(study)
    assert len(figure.data) == 1
    assert tuple(figure.data[0].x) == (0, 1)
    assert tuple(figure.data[0].y) == (1.0, 2.0)

    # Test with trials, one of which contains no intermediate value.
    study.optimize(lambda t: objective(t, False), n_trials=1)
    assert len(figure.data) == 1

    # Ignore failed trials.
    def fail_objective(_):
        # type: (Trial) -> float

        raise ValueError

    study.optimize(fail_objective, n_trials=1)
    assert len(figure.data) == 1
