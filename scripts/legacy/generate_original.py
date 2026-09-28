import random, string, re, os
import json
from logictree.io import read_jsonl, save_jsonl

class TreeNode:
    def __init__(self, val):
        self.val = val   #整个的表达式字符串
        self.sym = None  #二元计算符号 或 命题表达式
        self.left = None  #子节点
        self.right = None #子节点
        
def preorder_traversal(prop:TreeNode) -> list:
    result = []
    if prop.left!=None and prop.right!=None:
        result.append("(")
    if prop.left:
        result.extend(preorder_traversal(prop.left))
    result.append(prop.sym)
    if prop.right:
        result.extend(preorder_traversal(prop.right))
    if prop.left!=None and prop.right!=None:
        result.append(")")
    return result
def is_valid_parentheses(s: str) -> bool:
        stack = []

    # 遍历字符串中的每个字符
        for char in s:
            if char == ')':
            # 如果遇到闭括号，检查栈顶是否有匹配的开括号
                top_element = stack.pop() if stack else '#'
                if top_element != '(':
                    return False
            elif char == '(':
             # 如果是开括号，将其压入栈中
                stack.append(char)
        # 检查栈是否为空，空表示所有括号都匹配
        return not stack
def find_first_symbol(s:str) -> str:
        stack = []
        for i in range(len(s)):
            if s[i] == '(':
                stack.append(s[i])
            elif s[i] == ')':
                stack.pop()
            elif not stack and s[i] in ['>','&','|','⊕']:
                return i
            elif not stack and s[i] in ['~']:
                return i
        return -1    
def create_tree(s:str):
    prop = TreeNode(s)
    l = len(s)
    if s[0] == '(' and s[-1] == ')':
        if is_valid_parentheses(s[1:l-1]):
            s = s[1:l-1]
    index = find_first_symbol(s)
    if index == -1:
        # prop.sym = s
        return prop
    prop.sym = s[index]
    parts = [s[:index],s[index+1:]]
    if parts[0]:
        prop.left = create_tree(parts[0])
    # Create the right child node
    if parts[1]:
        prop.right = create_tree(parts[1])
    return prop

def format_equal(p1:TreeNode,p2:TreeNode):
    if p1 == None and p2 == None:
        return True
    elif (p1==None and p2!=None) or (p2==None and p1!=None):
        return False
    elif p1.sym != p2.sym:
        return False
    else:
        return format_equal(p1.left,p2.left) and format_equal(p1.right,p2.right)


def logic_tree_equal(l1,l2):
    if isinstance(l1,list) and isinstance(l2,list):
        n1 = len(l1)
        n2 = len(l2)
        if n1!=n2:
            return False
        else:
            for idx in range(n1):
                if not logic_tree_equal(l1[idx],l2[idx]):
                    return False
            return True
    elif isinstance(l1,list) != isinstance(l2,list):
        return False
    else:
        return format_equal(create_tree(l1),create_tree(l2))
    
    
def get_sub(s:str,subscript):
    a = subscript[s]
    subscript[s] += 1
    return s + f"{a}"

class LogicTreeNode:
    def __init__(self,p:str = None, sym:str = None, q:str = None):
        self.p, self.q = p, q
        self.sym = sym
        self.value = ""
        if sym is None:
            self.value += p
        elif sym in ['&','|','→','⊕']:
            self.value += p+sym+q
        elif sym == '~':
            self.value += sym+p
        self._clean_value()
        if self.value[0] == '(' and self.value[-1] == ')':
            if is_valid_parentheses(self.value[1:-1]):
                self.value = self.value[1:-1]
        index = find_first_symbol(self.value)
        if(index==-1):
            self.sym = None
            self.p = self.value
            self.q = None
        else:
            self.sym = self.value[index]
            if index == 0:
                self.p = self.value[1:]
                self.q = None
            else:
                part1 = self.value[0:index]
                part2 = self.value[index+1:]
                self.p = part1
                self.q = part2
        #self.p = '(' + p + ')' if p else p
        #self.q = '(' + q + ')' if q else q
        if not set(self.value).issubset((string.ascii_letters + string.digits)):
            self.value = "(" + self.value + ")"
        self.left = None
        self.right = None
        self.mid = None
        self.mark = None
    def _clean_value(self):
        cleaned_line = self.value.replace("~~", "")  # 替换掉连续的两个 ~
        cleaned_line = re.sub(r'~\(~\((.+)\)\)',r'\1',cleaned_line)
        cleaned_line = re.sub(r'~\(~([^\(\)&|~>⊕]+)\)',r'\1',cleaned_line) 
        if cleaned_line[0] == '(' and cleaned_line[-1] == ')' and set(cleaned_line[1:-1]).issubset(string.ascii_letters + string.digits):
            cleaned_line = cleaned_line[1:-1] 
        self.value = cleaned_line
    def _is_leaf(self):
        if self.left is None and self. right is None and self.mid is None:
            return True
        return False
    def first_order_clean(root,p):
        line1 = root.value
        line2 = root.p
        line3 = root.q
        cleaned_line1 = re.sub(p, p + r'(a)',line1)
        cleaned_line2 = re.sub(p, p + r'(a)',line2)
        if line3:
            cleaned_line3 = re.sub(p, p + r'(a)',line3)
        else:
            cleaned_line3 = None
        if root.mark != 0:
            root.value = cleaned_line1
            root.p = cleaned_line2
            root.q = cleaned_line3
        if root.left:
            LogicTreeNode.first_order_clean(root.left,p)
        if root.right:
            LogicTreeNode.first_order_clean(root.right,p)
        if root.mid:    
            LogicTreeNode.first_order_clean(root.mid,p)
    def _reformat_to_inode(self):#重新定义为独立的结点
        self.p = self.value
        self.q = None
        self.sym = None

    def _a2(self,p:str):
        new1 = LogicTreeNode(p,'→',self.value)
        new2 = LogicTreeNode(p)
        self.left = new1
        self.right = new2
    def _a2_1(self,p:str,q:str):
        new1 = LogicTreeNode(f"({p}&{q})",'→',self.value)
        new2 = LogicTreeNode(p)
        new3 = LogicTreeNode(q)
        new1.mark = 1
        self.left = new1
        self.right = new2
        self.mid = new3
    def _a2_2(self,p:str):
        newrule = f"∀x({p}(x)→{self.value}(x))"
        new2 = LogicTreeNode(f"{p}(a)")
        new1 = LogicTreeNode(newrule)
        new1.mark = 0
        self.left = new1
        self.right = new2
    def _a3(self,p:str):
        new1 = LogicTreeNode(p,'|',self.value)
        new2 = LogicTreeNode(p,'~')
        self.left = new1
        self.right = new2
    def _a3_2(self,p:str):
        newrule = f"∀x({p}(x)|{self.value}(x))"
        new2 = LogicTreeNode(f"{p}(a)","~")
        new1 = LogicTreeNode(newrule)
        new1.mark = 0
        self.left = new1
        self.right = new2
    def _a4(self,p:str):
        temp1 = LogicTreeNode(self.value,'~')
        new1 = LogicTreeNode(temp1.value,'→',p)
        new2 = LogicTreeNode(p,'~')
        self.left = new1
        self.right = new2
    def _a5_2(self,p):
        newrule = f"∀x({self.value}(x))"
        new1 = LogicTreeNode(newrule)
        new1.mark = 0
        self.left = new1
    def _b2(self,r:str):
        new1 = LogicTreeNode(self.p,'→',r)
        new2 = LogicTreeNode(r,'→',self.q)
        self.left = new1
        self.right = new2
    def _b2_2(self,r:str):
        newrule = f"(∀x(({self.p}(x)→{r}(x))&({r}(x)→{self.q}(x)))"
        new1 = LogicTreeNode(newrule)
        new1.mark = 0
        self.left = new1
    def _b3(self):
        temp1 = LogicTreeNode(self.p,'~')
        new1 = LogicTreeNode(temp1.value,'|',self.q)
        self.left = new1
    def _b4(self):
        temp1 = LogicTreeNode(self.q,'~')
        new1 = LogicTreeNode(self.p,'⊕',temp1.value)
        self.left = new1
    def _c2(self):
        temp1 = LogicTreeNode(self.p,'~')
        temp2 = LogicTreeNode(self.q,'~')
        temp3 = LogicTreeNode(temp1.value,'&',temp2.value)
        new1 = LogicTreeNode(temp3.value,'~')
        self.left = new1
    def _c3(self,p,r):
        new1 = LogicTreeNode(p,'→',self.p)
        new2 = LogicTreeNode(r,'→',self.q)
        new3 = LogicTreeNode(p,'|',r)
        self.left = new1
        self.right = new2
        self.mid = new3
    def _c4(self,q,s):
        temp1 = LogicTreeNode(self.p,'~')
        temp2 = LogicTreeNode(self.q,'~')
        new1 = LogicTreeNode(temp1.value,'→',q)
        new2 = LogicTreeNode(temp2.value,'→',s)
        temp3 = LogicTreeNode(q,'~')
        temp4 = LogicTreeNode(s,'~')
        new3 = LogicTreeNode(temp3.value,'|',temp4.value)
        self .left = new1
        self.right = new2
        self.mid = new3
    def _c5(self,p,s):
        new1 = LogicTreeNode(p,'→',self.p)
        temp1 = LogicTreeNode(self.q,'~')
        new2 = LogicTreeNode(temp1.value,'→',s)
        temp2 = LogicTreeNode(s,'~')
        new3 = LogicTreeNode(p,'|',temp2.value)
        self.left = new1
        self.right = new2
        self.mid = new3
    def _d2(self,p:str):
        new1 = LogicTreeNode(self.p,'→',p)
        new2 = LogicTreeNode(p,'~')
        self.left = new1
        self.right = new2
    def _d2_2(self,q:str):
        newrule = f"∀x({self.p}(x)→{q}(x))"
        new1 = LogicTreeNode(newrule)
        new2 = LogicTreeNode(f"{q}(a)","~")
        new1.mark = 0
        self.left = new1
        self.right = new2
    def _split(self,subscript,root,first_logic = False):
        #print("here")
        #对当前节点进行随机分裂
        if not self._is_leaf():
            return False
        
        if self.mark is not None:
            return False
        if self.sym is None:
            if set(self.p).issubset(string.ascii_letters + string.digits) and first_logic:
                chosen = random.choices([self._a2_2, self._a3_2, self._a5_2],weights=[0.2,0.3,0.5],k=1)
                chosen[0](get_sub('P',subscript))
                LogicTreeNode.first_order_clean(root,self.p)
            else:
                chosen = random.choices([self._a2,self._a2_1, self._a3, self._a4],weights=[0.3,0.2,0.3,0.2],k=1)
                if chosen[0] == self._a2_1:
                    chosen[0](get_sub('P',subscript),get_sub('P',subscript))
                else:
                    chosen[0](get_sub('P',subscript))
            return True
        elif self.sym == '→':
                chosen = random.choices([self._b2, self._b3, self._b4, "inode"],weights=[0.5,0.2,0,0.3],k=1)
                if chosen[0] == self._b2:
                    self._b2(get_sub('R',subscript))
                elif chosen[0] == "inode":
                    self._reformat_to_inode()
                    return self._split(subscript,root)
                else:
                    chosen[0]()
                return True
        elif self.sym == '|':
            chosen = random.choices([self._c2, self._c3, self._c4,self._c5, "inode"],weights=[0.2,0.2,0.2,0.2,0.2],k=1)
            if chosen[0] == self._c2:
                self._c2()
            elif chosen[0] == "inode":
                self._reformat_to_inode()
                return self._split(subscript,root)
            else:
                chosen[0](get_sub('Q',subscript),get_sub('T',subscript)) 
            return True
        elif self.sym == '~':
            if first_logic and set(self.p).issubset(string.ascii_letters + string.digits):
                chosen = random.choices([self._d2_2,self._d2,"inode"],weights=[0.0,0.5,0.5],k=1)
                if chosen[0] == self._d2 or chosen[0] == self._d2_2:
                    chosen[0](get_sub('S',subscript))
                elif chosen[0] == "inode":
                    self._reformat_to_inode()
                    return self._split(subscript,root)
            else:
                chosen = random.choices([self._d2,"inode"],weights=[0.5,0.5],k=1)
                if chosen[0] == self._d2:
                    self._d2(get_sub('S',subscript))
                elif chosen[0] == "inode":
                    self._reformat_to_inode()
                    return self._split(subscript,root)
            return True
        elif self.sym == '⊕':
            chosen = random.choices(["inode"],weights=[1],k=1)
            if chosen[0] == "inode":
                self._reformat_to_inode()
                return self._split(subscript,root)

    def node_split(self,prob:float,subscript,root,first_logic=False):#p为probability
        if not self._split(subscript,root,first_logic):
            return False
        return True

def find_leaves(root:LogicTreeNode) -> list:
    leaves = []
    if(root._is_leaf()):
        leaves.append(root)
    else:
        if root.left:
            leaves.extend(find_leaves(root.left))
        if root.right:
            leaves.extend(find_leaves(root.right))
        if root.mid:
            leaves.extend(find_leaves(root.mid))
    return leaves
def find_inode(root:LogicTreeNode) -> list:
    inode = []
    if root.left:
        inode.extend(find_inode(root.left))
    if root.right:
        inode.extend(find_inode(root.right))
    if root.mid:
        inode.extend(find_inode(root.mid))
    if not root._is_leaf():
        inode.append(root)
    return inode

def print_tree(root:LogicTreeNode,prefix="",pt=False)-> list:
    result = []
    result.append(root.value)
    if pt:
        print(prefix+root.value+'\n')
    kong = len(root.value)
    new_prefix = prefix + ' '*kong
    if root.left:
        result.append(print_tree(root.left,new_prefix,pt))
    if root.mid:
        result.append(print_tree(root.mid,new_prefix,pt))
    if root.right:
        result.append(print_tree(root.right,new_prefix,pt))
    return result
def leaf_to_str(leaf_list):
    leaves = []
    for leaf in leaf_list:
        leaves.append(leaf.value)
    return leaves
class LogicTree:
    def __init__(self) -> None:
        conclusion = random.choices(['~Q0','Q0','P0|Q0','P0→Q0'],weights=[0.3,3,0.2,0.2],k=1)[0]
        self.root = LogicTreeNode(conclusion)
        self.subscript={'P':1,'Q':1,'R':0,'S':0,'T':0,}
        self.split_order = []
    def _find_leaves(self):
        return find_leaves(self.root)
    def _find_inode(self):
        return find_inode(self.root)
    def _print_tree(self,pt=False):
        return print_tree(self.root,pt=pt)
    def _find_reasoning_process(self):
        res = []
        for node in self.split_order[::-1]:
            premises = []
            conclusion = node.value
            if node.left:
                premises.append(node.left.value)
            if node.mid:
                premises.append(node.mid.value)    
            if node.right:
                premises.append(node.right.value)
            res.append({
                "Premises":premises,
                "Conclusion":conclusion
                })
        return res
    def _random_leaf_split(self,prob,first_logic=False):
        #从所有的叶子节点里，任意选一个分裂
        leaves = self._find_leaves()
        a = random.choice(leaves)
        if first_logic:
            nosym = []
            for leaf in leaves:
                if leaf.sym is None:
                    nosym.append(leaf)
            if len(nosym) != 0 :a = random.choice(nosym)
        #print(a.value)
        while not a.node_split(prob,self.subscript,self.root,first_logic):
            leaves.remove(a)
            try:
                a = random.choice(leaves)
            except Exception as e:
                print("Can't find any node to split!")
                return
        self.split_order.append(a)
        return True
    
def random_split(T:LogicTree,num:int,p:float):
    for i in range(num):
        T._random_leaf_split(p)

def random_fol_split(T:LogicTree,num:int,p:float):
    if num<=3:
        fol_num = 1
    else:
        fol_num = 2
    for i in range(num-fol_num):
        T._random_leaf_split(p)
    for i in range(fol_num):
        T._random_leaf_split(p,first_logic=True)


# num表示分裂的次数 ？？？？
def dfs_split(conclusion:LogicTreeNode,num:int,p:float):
    a = conclusion
    for i in range(num):
        if a.random_split(p):
            if a.right:
                if a.mid:
                    a = random.choice([a.left,a.right,a.mid])
                else:
                    a = random.choice([a.left,a.right])
            else:
                a = a.left
        else:
            leaves = []
            find_leaves(conclusion,leaves)
            a = random.choice(leaves)
            while not a.random_split(p):
                leaves.remove(a)
                try:
                    a = random.choice(leaves)
                except Exception as e:
                    print("Can't find any node to split!")
                    return

def bfs_split(conclusion:LogicTreeNode,num:int,p:float,weight:float):
    a = conclusion
    for i in range(num):
        if random.random() < weight:
            leaves = []
            find_leaves(conclusion,leaves)
            a = random.choice(leaves)
            a.random_split(p)
        else:
            if a.right:
                if a.mid:
                    a = random.choice([a.left,a.right,a.mid])
                else:
                    a = random.choice([a.left,a.right])
            elif a.left:
                a = a.left
            a.random_split(p)
    
            
def clean_result(text):
    # 去掉连续的两个~符号
    cleaned_line = re.sub(r'~\(~\((.+)\)\)',r'\1',text) #
    cleaned_line = re.sub(r'\(~\(~([^\(\)&|~>⊕]+)\)\)',r'\1',cleaned_line) #
    cleaned_line = re.sub(r'~\(~([^\(\)&|~>⊕]+)\)',r'\1',cleaned_line)
    return cleaned_line
def clean_result_list(text_list):
    cleaned_list = []
    for text in text_list:
        cleaned_list.append(clean_result(text))
    return cleaned_list
def gen_multi_step_data(step,prob=0.3,pt=False):
    logictree = LogicTree()
    random_split(logictree,step,prob)
    res = logictree._print_tree(pt)
    reasoning_process = logictree._find_reasoning_process()
        
        #print(tree)
    leaves = leaf_to_str(logictree._find_leaves())
    inodes = leaf_to_str(logictree._find_inode())
        #print(leaves)
        #num+=1
    data={
            #"num": num,
        "step":step,
        "logic_tree":res,
        "leaf_nodes": leaves,
        "inodes":inodes,
            #"constraints":generate_natural_language_rules(leaves),
        "reasoning_process":reasoning_process
    }
    return  data

def gen_multi_step_fol_data(step,prob=0.3,pt=False):
    logictree = LogicTree()
    random_fol_split(logictree,step,prob)
    res = logictree._print_tree(pt)
    reasoning_process = logictree._find_reasoning_process()
        
        #print(tree)
    leaves = leaf_to_str(logictree._find_leaves())
    inodes = leaf_to_str(logictree._find_inode())
        #print(leaves)
        #num+=1
    data={
            #"num": num,
        "step":step,
        "logic_tree":res,
        "leaf_nodes": leaves,
        "inodes":inodes,
            #"constraints":generate_natural_language_rules(leaves),
        "reasoning_process":reasoning_process
    }
    return  data



def process_data(data):
    processed_data = []
    for item in data:
        rules = []
        for i,rule in enumerate(item["leaf_nodes"]):
            rules.append(f"rule{i+1}: {rule}.")
        reasoning_steps = []
        for i,step in enumerate(item["reasoning_process"]):
            premises = ", ".join(step["Premises"])
            conclusion = step["Conclusion"]
            reasoning_steps.append(f"step{i+1}: Given that [{premises}], it can be deduced that [{conclusion}].\n")
        #choice_question = random.choice(choice_template)
        #smallest_values = heapq.nsmallest(3, item["inodes"], key=len)
        option1_4 = item["inodes"][-4:]
        random.shuffle(option1_4)
        correct_option = [option1_4[0]]
        contradictory_option = [clean_result("~"+o) for o in option1_4[1:]]
        #unrelated_option = random.choice(["U","V","U>V","U|V","~U"])
        options = {
            "correct": correct_option,
            "uncorrect": contradictory_option,
        }
        processed_data.append({
            "num": item["num"],
            "step": item["step"],
            "logic_tree": item["logic_tree"],
            "leaf_nodes": item["leaf_nodes"],
            "inodes": item["inodes"],
            "rules": rules,
            "reasoning_steps": reasoning_steps,
            "options": options,
        })
    return processed_data

pre_data = read_jsonl()

data = []
save_dir = "./data/symbolic"

num = 0
same_num = 0
rule_times = [0,0,50,500,2000,4000,4000,3000,3000,2000,2000]
for s in range(2,11):
    i=0
    print(s)
    while i<rule_times[s]:
        logic_data = gen_multi_step_data(s,0.3)
        logic_data["num"] = num
        flag = True
        for d in pre_data:
            if d['step'] != s:
                continue
            if logic_tree_equal(d["logic_tree"],logic_data["logic_tree"]):
                same_num+=1
                flag = False
                break
        
        for d in data:
            if d['step'] != s:
                continue
            if logic_tree_equal(d["logic_tree"],logic_data["logic_tree"]):
                same_num+=1
                flag = False
                break
        if flag:
            data.append(logic_data)
            pre_data.append(logic_data)
            num+=1
            i+=1
print(same_num)
save_jsonl(data, os.path.join(save_dir,"rules_data_1116_1.jsonl"),"w")

