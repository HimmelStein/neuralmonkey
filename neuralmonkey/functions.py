import tensorflow as tf


def inverse_sigmoid_decay(param, rate, min_value=0., max_value=1.,
                          name=None, dtype=tf.float32):
    """Inverse sigmoid decay: k/(k+exp(x/k)).

    The result will be scaled to the range (min_value, max_value).

    Arguments:
        param: The parameter x from the formula.
        rate: Non-negative k from the formula.
    """

    with tf.name_scope(name, "InverseSigmoidDecay",
                       [rate, param, min_value, max_value]) as name:
        result = rate / (rate + tf.exp(param/rate))
        result = result * (max_value - min_value) + min_value
        result = tf.cast(result, dtype, name=name)

    return result


def piecewise_function(param, values, changepoints, name=None,
                       dtype=tf.float32):
    """A piecewise function.

    Arguments:
        param: The function parameter.
        values: List of function values (numbers or tensors).
        changepoints: Sorted list of points where the function changes from
            one value to the next. Must be one item shorter than `values`.
    """

    if len(changepoints) != len(values) - 1:
        raise ValueError("changepoints has length {}, expected {} (values "
                         "has length {})".format(len(changepoints),
                                                 len(values) - 1,
                                                 len(values)))

    with tf.name_scope(name, "PiecewiseFunction",
                       [param, values, changepoints]) as name:
        param = tf.convert_to_tensor(param)
        values = [tf.convert_to_tensor(y, dtype=dtype) for y in values]
        changepoints = [tf.convert_to_tensor(x, dtype=param.dtype)
                        for x in changepoints]

        predicates = [tf.less(param, x) for x in changepoints]
        lambdas = [lambda y=y: y for y in values]
        return tf.case(list(zip(predicates, lambdas[:-1])), lambdas[-1],
                       name=name)