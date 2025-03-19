
def markdown_to_blocks(markdown):
    block_list = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list

