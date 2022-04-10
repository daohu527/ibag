## design
How does rosbag read and differentiate messages?
1. Where the structure of the message is kept, msgs
2. Whether the message is out of order
3. How to convert msg to proto file

## prase bags

#### prase bags
1. we use below package to parse bags, ref [link](https://jmscslgroup.github.io/bagpy/Reading_bagfiles_from_cloud.html)
```
pip install bagpy
```

#### msg baseline
we should transform the `common_msgs` to proto format

#### gen proto py file
Then we should generate pyfiles for proto

#### do the transform
transform the msg and save to record.


## cyber record tools
how to make a cyber record file tools


## more general adaptation
For example, we need to convert message 1 to message 2, but their fields are different. We perform message conversion by allowing users to customize the conversion.

Pass in custom function. `add_transform(fun())`

