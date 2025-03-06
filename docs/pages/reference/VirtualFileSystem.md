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
post_metadata(fs_id: int, vfs_objects: list) -> list[JobDetails]
```
Add/Update/Remove Virtual File system Objects

Args:
* fs_id (int): Virtual file system id.
* vfs_objects (list): Virtual File System object list.

Returns:
* List of JobDetails: Status report of the executed background jobs.


## Examples

See `/examples/example_virtual_file_system.py`.