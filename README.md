# Houdini Interpreter
------
A method to make quick Houdini python scripts by `json` files.

## Structure
> **Node** `list`.
### Node
#### `id`: `int` 
- **Essential**.
- Negative `id` stands for the `-id` component in the current **selected** nodes.
- As two same `id` occurs, the new one will **overwrite** the previous one.
- If the length of selected nodes is smaller than the required negative `id`, it will fill in extra nodes by using the current **Network Editor** context.
#### `type`: `str`
- **Essential** when node `id` is **greater** than `0`.
- **Filter** node type when node `id` is **smaller** than `0`. If the node type **does not matches**, it will raise an Error.
#### `parentNodeContext`: `str`
- **Essential** when node `id` is **greater** than `0`.
- Only the following strings are **allowed**:
    - `node`: The `parentNodeId` node in `nodes` table.
    - `dopnet`: The current `DopNet`.
    - `parent`: The **parent node** of `parentNodeId` node in `nodes` table.
    - `obj`: The `obj` context.
#### `parentNodeId`: `int`
- **Essential** when node `id` is **greater** than `0` and `parentNodeContext` is `node` or `parent`.
#### `parms`: `list` of:
##### `name`: `str` 
- **Essential**.
##### `value`: `any` 
- **Essential**.
- Allow `int`, `float`, `bool` and `str`.
##### `oneTimeExperession`: `bool`
- Default `false`.
#### `inputs`: `list` of:
##### `nodeId`: `int`
- **Essential**.
- Negative `nodeId` for `spare inputs`.
##### `inputId`: `int`
- Default `0`.
##### `outputId`: `int`
- Default `0`.
#### `operations`: `dict` of:
##### `selected`: `bool`
- Default `false`. 
- If `true`, this node will **append** to the selection.
##### `forceSelected`: `bool`
- Default `false`. 
- If `true`, previous selection will be **deleted**.
##### `displayed`: `bool`
- Default `false`. 
- If `true`, set **display** flag enabled.
##### `rendered`: `bool`
- Default `false`. 
- If `true`, set **render** flag enabled.
##### `framed`: `bool`
- Default `false`. 
- If `true`, focus this node in **Network Editor**.