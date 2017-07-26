import tensorflow as tf


class TensorflowTest(tf.test.TestCase):
    def test_square(self):
        with self.test_session():
            x = tf.square([2, 3])
            self.assertAllEqual(x.eval(), [4, 9])


if __name__ == '__main__':
    tf.test.main()
