# A RouteTrie will store our routes and their associated handlers
class RouteTrie:
    def __init__(self,Root):
        # Initialize the trie with an root node and a handler, this is the root path or home page node
        self.root = RouteTrieNode(Root,None)

    def insert(self, path,handler):
        # Similar to our previous example you will want to recursively add nodes
        # Make sure you assign the handler to only the leaf (deepest) node of this path
        length = len(path)
        self.insert_helper(path,handler,0,self.root,length)

    def insert_helper(self,path,handler,counter,node,length):
        if node.child != [] :
            for i in node.child:
                if i.value == path[counter]:
                    return self.insert_helper(path,handler, counter + 1, i, length)

        temp = RouteTrieNode(path[counter], None)
        if length - 1 > counter:
            node.child.append(temp)
            return self.insert_helper(path,handler, counter + 1, temp, length)
        else:
            temp.handler = handler
            node.child.append(temp)

    def find(self,path):
        # Starting at the root, navigate the Trie to find a match for this path
        # Return the handler for a match, or None for no match
        if path == "/":
            return self.root.value
        length = len(path)
        return self.find_helper(path,self.root,length,0,0)
    def find_helper(self,path,node,length,index,count):
        for i in node.child :
            temp = None
            if index < length:
                if i.value == path[index]:
                    temp = i
                    count = count + 1
                    return self.find_helper(path, temp,length, index + 1, count)
            else:
                break
        if len(path) == count :
            return node.handler
        else:
            return None

# A RouteTrieNode will be similar to our autocomplete TrieNode... with one additional element, a handler.
class RouteTrieNode:
    def __init__(self, value,handler):
        # Initialize the node with children as before, plus a handler
        self.value = value
        self.handler = handler
        self.child = []

class Router:
    def __init__(self,root):
    # Create a new RouteTrie for holding our routes
    # You could also add a handler for 404 page not found responses as well!
        self.router = RouteTrie(root)

    def add_handler(self,path,handler):
    # Add a handler for a path
    # You will need to split the path and pass the pass parts
    # as a list to the RouteTrie
        path = self.split_path(path)
        self.router.insert(path,handler)

    def lookup(self,path):

    # lookup path (by parts) and return the associated handler
    # you can return None if it's not found or
    # return the "not found" handler if you added one
    # bonus points if a path works with and without a trailing slash
    # e.g. /about and /about/ both return the /about handler
        if len(path) > 1:
            path = self.split_path(path)
        return self.router.find(path)

    def split_path(self,path):
        # you need to split the path into parts for
        # both the add_handler and loopup functions,
        # so it should be placed in a function here
        path = path.split("/")
        for i in path :
            try :
                path.remove("")
            except:
                continue

        return path




# r = RouteTrie()
# path = "/b/c/d"
# path = path.split("/")
# path.remove("")
# r.insert(path,"o")
#
# path1 = "/a/c/d"
# path1 = path1.split("/")
# path1.remove("")
# r.insert(path1,"m")
#
# path1 = "/a/b/f"
# path1 = path1.split("/")
# path1.remove("")
# r.insert(path1,"l")
# print(r.find(["a","c","d"]).handler)
# print(r.root.child[1].child[1].child[0].handler)
# Here are some test cases and expected outputs you can use to test your implementation

# create the router and add a route
router = Router("root handler")  # remove the 'not found handler' if you did not implement this
router.add_handler("/home/about", "about handler")  # add a route
# # some lookups with the expected output
print(router.lookup("/"))  # should print 'root handler'
print(router.lookup("/home"))  # should print 'not found handler' or None if you did not implement one
print(router.lookup("/home/about"))  # should print 'about handler'
print(router.lookup("/home/about/"))  # should print 'about handler' or None if you did not handle trailing slashes
print(router.lookup("/home/about/me"))  # should print 'not found handler' or None if you did not implement one