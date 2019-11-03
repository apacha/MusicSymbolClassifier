import tensorflow as tf


class TensorflowTest(tf.test.TestCase):
    def test_square(self):
        x = tf.square([2, 3])
        self.assertAllEqual(x.numpy(), [4, 9])


if __name__ == '__main__':
    tf.test.main()
