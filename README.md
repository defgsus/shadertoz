# Shadertox

Momentarily, this is just a django project that accesses the 
[shadertoy.com](https://shadertoy.com) [API](https://www.shadertoy.com/api).

If time permits, it will get more interesting...

## usage

Download shaders and store to db.
```bash
./manage.py shadertox_download_shadertoy
```

Update shader models from json values, in case you've added some fields
to `shaders.models.ShadertoyShader`. 
```bash
./manage.py shadertox_update_shadertoy_model
```
