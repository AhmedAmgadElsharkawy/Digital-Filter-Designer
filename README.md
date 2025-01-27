# Digital-Filter-Designer
A desktop app for real-time digital filter design, allowing users to place and manipulate zeros and poles, visualize frequency responses, apply filters to signals, and generate C code. Features include an all-pass filter library, customizable realizations, and interactive signal input.


# Development Setup

1. create virual environmet
```
    python -m venv digital_filter_designer_venv
```

2. activate the virtual environment

```
    digital_filter_designer_venv\Scripts\activate
```
3. install requiremnets modules

```
    pip install -r requirements.txt
```

# Note

<div style="color: red; font-weight: bold; font-size:20px;">
    freeze the modules after installing a new one to make the code reproducible (<span style = "text-decoration:underline;">make sure that the venv is activated at first</span>)
</div>

```
    pip freeze > requirements.txt
```
