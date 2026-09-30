# Payment incident

Customers are getting the wrong change when they pay.

Inspect `apply_payment` in `app/checkout.py`. A 4.50 order paid with 10.00 currently does not return 5.50.

Fix the calculation on this branch. The unfinished tax work on `feature/checkout` is not ready to ship, and it needs to stay available.
