# Train `logreg`

We'll train the `logreg` model with one epoch. Noe that we
don't have to specify the full model name as long as our term refers
to one and only one model.

    >>> run("guild run -y --no-gpus logreg:train epochs=1",
    ...     ignore=["Successfully downloaded", "^INFO: ", "FutureWarning"])
    Limiting available GPUs (CUDA_VISIBLE_DEVICES) to: <none>
    Resolving mnist-dataset dependency
    ...
    Step 20: training=...
    Step 20: validate=...
    ...
    Step 550: training=...
    Step 550: validate=...
    Saving checkpoint...
    <exit 0>
