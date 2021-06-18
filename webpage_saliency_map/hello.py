def getSiblingElementIndex(el, name):
  index = 1
  sib = el
  while sib = sib.previousElementSibling:
    if sib.nodeName.toLowerCase() == name:
      ++index
  return index

def getSelectorFromElement(element):
  names = []
  if !(el instanceof Element):
    return names
  while el.nodeType == 1:
    name = el.nodeName.toLowerCase()
    if el.id:
      name += '#' + el.id
      names.unshift(name)
      break
    index = getSiblingElementIndex(el, name)
    if(1 < index) {
      name += ':nth-of-type(' + index + ')'
    }
    names.unshift(name)
    el = el.parentNode
  return names.join(" > ")
