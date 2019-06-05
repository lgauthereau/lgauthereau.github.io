def method_one():
        print("look I'm a method")
def method_two(name):
        #because it is executed in line 8, name is defined as "Brandon"
        print("about to call our first method for " + name)
        method_one()
        #above is where the method is inside the method
method_two("Brandon")
