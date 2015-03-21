'''
Created on Mar 13, 2015

@author: Alice
'''


def birth(parent, child):
    '''
    
    :param parent:
    :type parent:
    :param child:
    :type child:
    '''
    COMMENT = "t1"
    LINK = "t3"
    AUTHOR = "t2"
    SUBREDDIT = "t5"
    DIRECT_PARENT = "dir_parent"   
    if not isinstance(child, T):
        raise Exception("Child is not an instance of T")
    if not (child.kind == COMMENT or child.kind == LINK):
        raise Exception("Child is not of type comment or link")
    if not (child.parent_id == parent.id or child.author == parent.id or child.link_id == parent.id):
        raise Exception("Child does not declare this as a parent or author or link")
    if parent.kind == AUTHOR:
        child.add_author(parent)
    elif parent.kind == LINK:
        child.add_link(parent)
    if parent.id == child.parent_id:
        child.add_direct_parent(parent)
        parent.add_child(child)
COMMENT = "t1"
LINK = "t3"
AUTHOR = "t2"
SUBREDDIT = "t5"
DIRECT_PARENT = "dir_parent"   
class T(object):
    '''
    Base class for T objects, can have children, direct parents, and links
    as wee as an id, kind, and a created_utc
    '''

    
    def __init__(self, idd, kind, created_utc):
        '''
        
        :param idd: This id (name if author)
        :type idd: String if author, else Long
        :param kind: this kind (t1/t2/t3/t5)
        :type kind: String
        :param created_utc: when this was created
        :type created_utc: long
        '''
        self.__children = {}
        self.__parent = {}
        self.id = idd
        self.kind = kind
        self.created_utc = created_utc 
    def add_author(self, author):
        '''
        used to build trees
        add author to this' parents
        :param author:
        :type author:
        '''
        self.__parent[AUTHOR] = author
    def add_link(self, link):
        '''
        used to build trees
        add link to this' link
        :param link: 
        :type link:
        '''
        self.__parent[LINK] = link
    def add_direct_parent(self, direct_parent):
        '''
        used to build trees
        add direct parent to this' direct parent
        :param direct_parent:
        :type direct_parent:
        '''
        self.__parent[DIRECT_PARENT] = direct_parent
    def add_child(self, child): 
        '''
        used to build trees
        add a child to this' children
        :param child:
        :type child:
        '''
        self.__children[child.id] = child   
    def get_link(self):
        '''
        return link this is attached to if known, else None
        '''
        if T.LINK in self.parent:
            return self.parent[T.LINK]
        return None 
    
    def children(self):
        '''
        Shallow
        :return a shallow copy array of this' children
        '''
        changlings = {}
        for child_key, child in self.__children.iteritems():
            changlings[child_key] = child
        return changlings
    def parent(self):
        '''
        Shallow
        :return this' parent
        '''
        stahpit_mom = {}
        for parent_key,parent_object in self.__parent.iteritems():
            stahpit_mom[parent_key] = parent_object
        return stahpit_mom
    def is_direct_parent_of(self, child):
        '''
        Determine if this is a direct parent of that child
        :param child: 
        :type child: TBase
        :return boolean
        '''
        return child.id in self.__children
    
    def __eq__(self, other):
        '''
        equality determined by id
        :param other: 
        :type other: Object
        :return boolean
        '''
        return isinstance(other, T) and other.id == self.id
    def __ne__(self, other):
        '''
        Not equals determined by ID
        :param other:
        :type other: Object
        '''
        return not self.__eq__(other)
           

        
    
        