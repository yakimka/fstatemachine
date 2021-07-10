.. fstatemachine documentation master file, created by
   sphinx-quickstart on Fri Jul  9 21:41:57 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to fstatemachine's documentation!
=========================================

fstatemachine is a simple finite state machine implementation written in Python.
It supports python >= 3.6

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`search`



Installation
============

.. code-block::

    pip install fstatemachine

or clone the repo and execute:

.. code-block::

    python setup.py install

Quickstart
==========

.. code-block:: python

    from fstatemachine import StateMachine

    # Define some states, order is not important
    order_states = ['pending', 'awaiting_payment', 'shipped', 'cancelled', 'completed']
    # Or with aliases
    # order_states = {1: 'pending', 2: 'awaiting_payment', 3: 'shipped', 4 : 'cancelled', 5: 'completed'}
    # order_states = [(1, 'pending'), (2, 'awaiting_payment'), (3, 'shipped'), (4, 'cancelled'), (5, 'completed')]

    # Define transitions
    order_transitions = {
        # Order status can be changed from pending to any other state
        'pending': '__all__',
        # awaiting_payment cannot be changed again to pending, but can be any another
        'awaiting_payment': ['shipped', 'cancelled', 'completed'],
        # from shipped we can change state only to cancelled or completed
        'shipped': ['cancelled', 'completed'],
        # we cannot change status from cancelled or completed
        # we just didn't specify the dictionary key,
        # but this will do the same:
        # 'cancelled': None,
        # 'completed': [],
    }

Now we can play with this example

.. code-block:: python

    >>> machine = StateMachine(current='pending', states=order_states, transitions=order_transitions)
    >>> # we can check ability to change the state
    >>> machine.check('cancelled')
    >>> # or we can set new state and check that it is legit in one action
    >>> machine.current = 'shipped'  # change state from pending to shipped
    >>> # this will raise WrongTransition exception
    >>> machine.check('pending')
    WrongTransition: from shipped to pending
    >>> # and this
    >>> machine.current = 'awaiting_payment'
    WrongTransition: from shipped to awaiting_payment


Package contents
================

The ``StateMachine`` class
*****************************
.. autoclass:: fstatemachine.StateMachine
    :members:
    :undoc-members:


The ``WrongTransition`` exception
*********************************
.. autoexception:: fstatemachine.WrongTransition
    :members:
    :undoc-members:
