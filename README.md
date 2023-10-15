# 3D sketch -> 3D model

## Environment
This project is build in MacOS, but Windows/linux should work well.
```bash
pip install image
pip install imath
```

For MacOS, you could
```bash
brew install openexr

# These environment variables are required for OpenEXR pip package to compile
export CFLAGS="-I/opt/homebrew/include/OpenEXR -I/opt/homebrew/include/Imath -std=c++11"
export LDFLAGS="-L/opt/homebrew/lib"

pip install openexr
```


## Steps

1. Genrate Multi-view Depth Image from Model.
```bash
blender -b -P render_depth.py
```
The results are stored in `./output`
2. Visualize the EXR results
```bash
python plot_exr.py
```


## Reference

+ https://www.guyuehome.com/41655