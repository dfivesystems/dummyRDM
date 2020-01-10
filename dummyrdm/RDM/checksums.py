def rdmCheckSum(checksumbytes):
    checksum = sum(checksumbytes)
    checksumbytes.extend((checksum // 256, checksum % 256))
    return checksumbytes