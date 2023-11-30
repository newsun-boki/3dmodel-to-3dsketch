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
#source ~/.bash_profile
blender -b -P render_depth.py
```
The results are stored in `./output`
2. Visualize the EXR results to get the depth image
```bash
python plot_exr.py
```
3. Apply edge detection and get depth image and final point cloud

```bash
python precess_exr.py
```
4. combine all point cloud, downsampling,remove noise

```bash
python combine_points.py
```

5. generate 3d curve from ply

```bash
python ply2curve.py
```

## Reference

+ https://www.guyuehome.com/41655