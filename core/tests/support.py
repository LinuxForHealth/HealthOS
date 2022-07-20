import os

# base resource directory for "file fixtures"
resources_directory = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "resources",
)


class AsyncIterator:
    """
    Class used to provide a reasonable mock for async iterators
    """

    def __init__(self, iterable_object):
        """
        Configures the AsyncIterator instance.

        :param iterable_object: An iterable object which supports the "iter" protocol.
        """
        self.iter = iter(iterable_object)

    def __aiter__(self):
        """For beginning async iteration"""
        return self

    async def __anext__(self):
        """Returns the next item from the async iterator"""
        try:
            return next(self.iter)
        except StopIteration:
            raise StopAsyncIteration
