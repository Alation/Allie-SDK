---
title: Virtual File System
parent: SDK Reference
---

# Virtual File System
{:.no_toc}

* TOC
{:toc}

## Models

### VirtualFileSystemItem
Python object used for creating file system entries like files and directories, and passed as a list in the function `post_metadata`.

Attributes:

| Name         | Required | Type                  | Description                                                  |
|--------------|:--------:|-----------------------|--------------------------------------------------------------|
| path |  TRUE    | str         | Absolute path to the file. (default is /). |
| name |  TRUE    | str         | Name of the file or directory. |  
| is_directory |  TRUE    | bool         | Indicates if the object is a directory or file.  |  
| size_in_bytes |  FALSE    | int         | The size of the file or directory in bytes. | 
| ts_last_modified |  FALSE    | str         | Timestamp that the file was last modified. <br>Format must be YYYY-mm-dd HH:MM:SS. Timezone is UTC. | 
| ts_last_accessed |  FALSE    | str         | Timestamp that the file was last accessed. <br>Format must be YYYY-mm-dd HH:MM:SS. Timezone is UTC. | 
| owner |  FALSE    | str         | Name of the user that owns the object. | 
| group |  FALSE    | str         | Name of the group. | 
| permission_bits |  FALSE    | int         | Unix style file permissions. <br>Must be three Octal digits. Ex. 755 | 
| storage_type |  FALSE    | int         | Indicates the S3 storage type.<>Only used for S3 file systems.<br>0 - Standard<br>1 - Standard IA<br>2 - Reduced REdundancy<br>3 - Glacier |

## Methods
### post_metadata

```
post_metadata(fs_id: int, vfs_objects: list) -> bool
```
Add/Update/Remove Virtual File system Objects

Args:
* fs_id (int): Virtual file system id.
* vfs_objects (list): Virtual File System object list.

Returns:
* boolean: Success/Failure of the API POST Call(s).


## Examples
### Post Virtual File System Objects Add/Update
```python
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

# Add/Update Objects   
fs_id = 42
vfs_objects = []
vfs_objects.append(allie.VirtualFileSystemItem(path="/", name="var", is_directory=True))
vfs_objects.append(allie.VirtualFileSystemItem(path="/var", name="log", is_directory=True,  size_in_bytes=8800,
                                               owner="root", group="root",
                                               permission_bits=755))
vfs_objects.append(allie.VirtualFileSystemItem(path="/var", name="File 2", is_directory=False, size_in_bytes=120))
vfs_objects.append(allie.VirtualFileSystemItem(path="/var/log", name="boot.log", is_directory=False, 
                                               size_in_bytes=600,
                                               ts_last_modified="2024-06-20T18:26:54.663432Z",
                                               ts_last_accessed="2024-06-20T18:26:54.663432Z", 
                                               owner="root", group="root",
                                               permission_bits=755))
vfs_objects.append(allie.VirtualFileSystemItem(path="/var/log", name="access.log", is_directory=False, 
                                               size_in_bytes=280,
                                               ts_last_modified="2024-06-20T18:26:54.663432Z",
                                               ts_last_accessed="2024-06-20T18:26:54.663432Z", 
                                               owner="root", group="root",
                                               permission_bits=755))

vfs_response = alation.virtual_filesystem.post_metadata(fs_id=fs_id, vfs_objects=vfs_objects)
```

### Post/Remove All Virtual File System Objects
```python
# Remove All Objects   
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

fs_id = 42
vds_response = alation.virtual_filesystem.post_metadata(fs_id=fs_id, vfs_objects=[])

```
### Post/Remove Unmentioned Virtual File System Objects
```python
# Remove All Objects   
import allie_sdk as allie

alation = allie.Alation(
    host='<HOST>',
    user_id=<USER_ID>,
    refresh_token='<REFRESH_TOKEN>')

fs_id = 42
vfs1 = allie.VirtualFileSystemItem(path="/", name="var", is_directory=True)
# All other file objects that are not part of the vfs_objects list will be deleted 
vds_response = alation.virtual_filesystem.post_metadata(fs_id=fs_id, vfs_objects=[vfs1])

```