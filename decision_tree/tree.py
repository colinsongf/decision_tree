import math

class Builder:
	def build(self, examples):
		"""builds the tree"""
		
		"""attribute names are simply the index of the attribute in the examples"""
		i, attributes = 0, []
		for col in examples[0][0:-1]:
			attributes.append(i)
			i += 1
		return self.learn(examples, attributes, examples)
	
	def learn(self, examples, attributes, parent_examples):
		"""decision tree algorithm"""
		if len(examples) == 0:
			return Leaf(self.plurality(parent_examples))
		elif self.same_classification(examples):
			return Leaf(examples[0][-1])
		elif len(attributes) == 0:
			return Leaf(self.plurality(examples))
		else:
			best = self.best_attribute(attributes, examples)
			sub_attributes = attributes[:]
			sub_attributes.remove(best)
			tree = Node(best)
			partitions = self.partition(examples, best)
			for key, sub_examples in partitions.iteritems():
				tree.add_child(key, self.learn(sub_examples, sub_attributes, examples))
			return tree
	
	def partition(self, examples, best):
		"""breaks up the examples based upon the value they have for the attribute specified"""
		partitions = {}
		for example in examples:
			key = example[best]
			if partitions.get(key):
				partitions.get(key).append(example)
			else:
				partitions[key] = [example]
		return partitions
			
	def same_classification(self, examples):
		"""checks if all the examples have the same classification"""
		classification = None
		for row in examples:
			if not classification:
				classification = row[-1]
			elif classification != row[-1]:
				return False
		return True
	
	def plurality(self, examples):
		"""finds the majority class label for the examples"""
		high = examples[0][-1]
		counts = {high: 0}
		for row in examples:
			label = row[-1]
			if counts.get(label):
				counts[label] += 1
				if counts[label] > counts[high]:
					high = label
			else:
				counts[label] = 0
		return high
	
	def best_attribute(self, attributes, examples):
		"""selects the best attribute for the examples based upon the highest change in entropy"""
		best = attributes[0]
		best_change = self.entropy_change(examples, 0)
		for attr in attributes[1:]:
			change = self.entropy_change(examples, attr)
			if change > best_change:
				best = attr
				best_change = change
		return best
	
	def entropy_change(self, examples, attribute):
		"""entropy of all the examples minus entropy of the examples split by the attribute specified"""
		return self.non_split_entropy(examples) - self.split_entropy(examples, attribute)
	
	def non_split_entropy(self, examples):
		"""entropy of all the examples"""
		label_counts = {}
		for example in examples:
			if label_counts.get(example[-1]):
				label_counts[example[-1]] += 1
			else:
				label_counts[example[-1]] = 1
		return self.entropy(label_counts, len(examples))
	
	def split_entropy(self, examples, attribute):
		"""entropy of the examples split by the attribute specified"""
		partitions = self.partition(examples, attribute)
		entropy = 0
		for k, ex in partitions.iteritems():
			en = self.non_split_entropy(ex)
			entropy += (len(ex) / float(len(examples))) * en
		return entropy
	
	def entropy(self, label_counts, total):
		"""calculates the entropy"""
		entropy = 0
		for label, count in label_counts.iteritems():
			frac = count / float(total)
			part = 0
			if frac != 0:
				part = frac * math.log(frac, 2)
			entropy += part
		return part * -1

class Node:
	def __init__(self, attribute):
		"""a decision node"""
		self.attribute = attribute
		self.children = {}
		
	def add_child(self, value, node):
		"""adds a child node for the specified value of this attribute"""
		self.children[value] = node
		
	def choose(self, example):
		"""chooses a label based on the examples attribute"""
		return self.select_child(example).choose(example)
	
	def select_child(self, example):
		if self.children.get(example[self.attribute]):
			return self.children[example[self.attribute]]
		else:
			"""if we have never seen the attribute, the tree doesn't know how to handle it."""
			"""we generate a junk value so that it will be considered a miss."""
			return Leaf('')
		
	def number_of_nodes(self):
		"""the number of nodes in the children trees plus this node"""
		num = 1
		for k, v in self.children.iteritems():
			num += v.number_of_nodes()
		return num
	
	def to_s(self, depth=1):
		"""visualizes the tree"""
		s = "%i\n" % (self.attribute)
		for k, v in self.children.iteritems():
			s = "%s%s%s: %s" % (s, "  " * depth, k, v.to_s(depth + 1))
		return s

class Leaf:
	def __init__(self, choice):
		"""represents a class label choice"""
		self.choice = choice
	
	def choose(self, example=None):
		"""returns the class label"""
		return self.choice
	
	def number_of_nodes(self):
		"""return the number of nodes"""
		return 1
	
	def to_s(self, depth):
		"""visualizes the leaf"""
		return "%s\n" % (self.choice)