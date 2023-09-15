# # import ProductionRule
import sys
import copy
from pathlib import Path
from enum import Enum
import os
import shutil
import subprocess

class ProductionRule:           #Tested

    def __init__(self, LHS):
        self.LHS = LHS
        self.RHS = []
    
    def __str__(self):
        return  f"{self.LHS} -> {self.RHS} "
    
    def addRHS(self, RHS):
        self.RHS.append(RHS)
    
    def addRHSall(self,RHSall):
        for i in RHSall:
            self.addRHS(i)
    
    def getLHS(self):
        return self.LHS
    
    def getRHS(self):
        return self.RHS
    
    def setnewRHS(self, RHS):
        self.RHS.clear()
        self.addRHSall(RHS)

    def printProductionRule(self):
        print(f"{self.LHS} -> ")
        s = ""
        for right in self.RHS:
            s = s + " " + right + " |"
        s.replace(s[len(s)-1], "")
        print(s)

    def __eq__(self, other):
        if other == None:
            return False
        return self.LHS == other.LHS

class Grammar:                   
    epsilon = '\u03B5'
    end_of_line = "$"
    firstSymbol = ""

    def __init__(self) -> None:         #Tested
        self.production_rule = []           #list of ProductionRule
        self.terminal_symbols = []
        self.non_terminal_symbols = []
        self.terminal_symbols.append(self.end_of_line)
        self.firstSet = {}
        self.followSet = {}   

    def __str__(self) -> str:           # Tested
        s = ""
        for i in self.production_rule:
            s += i.__str__()
        return s

    def getFirstSymbol(self):           # Tested
        return self.firstSymbol
    
    def setFirstSymbol(self, firstSymbol):      # Tested
        self.firstSymbol = firstSymbol

    def getProductionRules(self):           # Tested
        return self.production_rule
    
    def getProductionRulesBasedOnNonTerminal(self, symbol):     # Tested
        rule = ProductionRule(symbol)
        if rule in self.production_rule:
            index = self.production_rule.index(rule)
            return self.production_rule[index]
        else:
            return None

    def addRuleList(self, LHS, RHS):           # Tested
        alreadyExistingRule = self.getProductionRulesBasedOnNonTerminal(LHS)

        if alreadyExistingRule is None:
            newProductionRule = ProductionRule(LHS)
            newProductionRule.addRHSall(RHS)
            self.production_rule.append(newProductionRule)
        else:
            alreadyExistingRule.addRHS(RHS)

    def addRule(self, input):               # Tested
        rulesplit = input.split("->")
        left_side = rulesplit[0]
        left_side = left_side.strip()
        right_side = rulesplit[1].split("|")

        rightfinal = []
        for right in right_side:
            right = right.strip()
            symbols = right.split(" ")
            rightfinal.append(symbols)
        self.addRuleList(left_side, rightfinal)

    def getTerminalSymbols(self):           # Tested
        return self.terminal_symbols
    
    def getNonTerminalSymbols(self):        # Tested
        return self.non_terminal_symbols
    
    def addAllTerminalSymbolFromIterator(self, iterator):       # Tested
        for symbol in iterator:
            self.addTerminalSymbol(symbol)

    def addAllNonTerminalSymbolFromIterator(self, iterator):    # Tested
        for symbol in iterator:
            self.addNonterminalSymbol(symbol)
        
    def addTerminalSymbol(self, str):            # Tested
        if str not in self.terminal_symbols:              
            self.terminal_symbols.append(str)

    def addNonterminalSymbol(self, str):                # Tested
        self.non_terminal_symbols.append(str)
    
    def isTerminalSymbol(self, str):            # Tested
        if str not in self.terminal_symbols:
            return False
        return True
    
    def isNonterminalSymbol(self, str):         # Tested
        if str not in self.non_terminal_symbols:
            return False
        return True
    
    def addFirstSet(self, symbol, firstSetSymbols):         # Tested          
        if symbol in self.firstSet:
            self.firstSet[symbol].append(firstSetSymbols)
        else:
            toAdd = []
            toAdd.append(firstSetSymbols)
            self.firstSet[symbol] = toAdd
        self.firstSet[symbol] = list(dict.fromkeys(self.firstSet[symbol]))

    def addAllFirstSet(self, symbol, firstSet):         # Tested
        for first in firstSet:
            self.addFirstSet(symbol, first)

    def getFirstSet(self, symbol):              # Tested
        if symbol not in self.firstSet.keys():
            return None
        return copy.deepcopy(self.firstSet[symbol])

    def computeFirstSetForparticularSymbol(self, symbol):   # Tested
        if self.isTerminalSymbol(symbol):
            result = []
            result.append(symbol)
            return result
        
        # production_rule = ProductionRule(symbol)
        production_rule = self.getProductionRulesBasedOnNonTerminal(symbol)
        
        assert production_rule is not None

        result = []
        for right in production_rule.getRHS():
            if right[0] == self.epsilon:
                result.append(self.epsilon)
            else:
                toAddEpsilon = True
                for symbolRS in right:
                    toAdd = self.computeFirstSetForparticularSymbol(symbolRS).copy()
                    if self.epsilon in toAdd:
                        toAdd.remove(self.epsilon)  
                        result.extend(toAdd)
                    else:
                        toAddEpsilon = False
                        result.extend(toAdd)
                        break

                if toAddEpsilon:
                    result.append(self.epsilon)
        return result

    def computeFirstSetForAllTerminalSymbols(self):         # Tested
        for terminal in self.terminal_symbols:
            if terminal == self.end_of_line:
                continue
            self.addFirstSet(terminal, terminal)

    def computeFirstSetforAllNonTerminalSymbols(self):          # Tested
        for nonterminal in self.non_terminal_symbols:
            toAdd = self.computeFirstSetForparticularSymbol(nonterminal)
            # print(nonterminal, toAdd)
            self.addAllFirstSet(nonterminal, toAdd)
    
    def computeFirstSetforAllSymbols(self):                     # Tested
        self.computeFirstSetForAllTerminalSymbols()
        self.computeFirstSetforAllNonTerminalSymbols()

    def addFollowSet(self, symbol, followSetSymbol):            # Tested
        if symbol in self.followSet:
            self.followSet[symbol].append(followSetSymbol)
        else:
            toAdd = []
            toAdd.append(followSetSymbol)
            self.followSet[symbol] = toAdd
        self.followSet[symbol] = list(dict.fromkeys(self.followSet[symbol]))

    def addAllFollowSet(self, nonTerminal, followSet):          # Tested
        for follow in followSet:
            self.addFollowSet(nonTerminal, follow)

    def getFollowSet(self, symbol):                             # Tested
        if symbol not in self.followSet.keys():
            return None
        return copy.deepcopy(self.followSet[symbol])
    
    def computeFollowSetForNonTerminalSymbol(self, nonTerminal):    # Tested
        result = []

        if nonTerminal == self.firstSymbol:
            result.append(self.end_of_line)
        
        for productionrule in self.production_rule:
            LHS = productionrule.getLHS()
            
            for right in productionrule.getRHS():
                for i in range(len(right)):
                    symbol = right[i]

                    if symbol == nonTerminal:
                        if i == (len(right) - 1):
                            if LHS == nonTerminal:
                                continue
                            else:
                                result.extend(copy.deepcopy(self.computeFollowSetForNonTerminalSymbol(LHS)))
                        else: 
                            firstOfNext = self.getFirstSet(right[i+1])
                            if self.epsilon in firstOfNext:
                                firstOfNext.remove(self.epsilon)
                                result.extend(copy.deepcopy(firstOfNext))
                                result.extend(copy.deepcopy(self.computeFollowSetForNonTerminalSymbol(LHS)))
                            else:
                                result.extend(copy.deepcopy(firstOfNext))
        return result
    
    def computeFollowSetForAllSymbols(self):                    # Tested
        for nonTerminal in self.non_terminal_symbols:
            toAdd = self.computeFollowSetForNonTerminalSymbol(nonTerminal)
            self.addAllFollowSet(nonTerminal, toAdd)

    def computeFirstAndFollowForAllSymbols(self):               # Tested
        self.computeFirstSetforAllSymbols()
        self.computeFollowSetForAllSymbols()

    def printFirstandFollowSet(self):       # Tested
        print("First Set: ")
        for i in self.firstSet.keys():
            print("{} -> {}".format(i, self.firstSet[i]))

        print("Follow Set: ")
        for i in self.followSet.keys():
            print("{} -> {}".format(i, self.followSet[i]))
    
    def printGrammar(self):             # Tested
        print("Set of terminal symbols: {}".format(str(self.terminal_symbols)))
        print("Set of non_terminal symbols: {}".format(str(self.non_terminal_symbols)))
        print("Rules of Grammar: ")
        for i in self.production_rule:
            print(i)

    def printGrammarWithToFile(self, pathToDirectory, note):
        pathToFile = os.path.join(pathToDirectory, note.replace(" ", "") + ".txt")

        with open(pathToFile, 'w', encoding='utf-8') as writer:
            writer.write(note + "\n")
            writer.write("Set of Terminal Symbols: " + str(self.terminal_symbols) + "\n")
            writer.write("Set of Non-Terminal Symbols: " + str(self.non_terminal_symbols) + "\n")
            writer.write("Rules in the given Grammar: \n")

            for productionRule in self.production_rule:
                writer.write(str(productionRule) + "\n")

    def printFirstAndFollowSetToFile(self, pathToDirectory, note):
        pathToFile = os.path.join(pathToDirectory, note.replace(" ", "") + ".txt")

        with open(pathToFile, "w", encoding='utf-8') as writer:
            writer.write("First Set: \n")
            for key, value in self.firstSet.items():
                writer.write(key + " -> " + str(value) + "\n")
            writer.write("\n")

            writer.write("Follow Set: \n")
            for key, value in self.followSet.items():
                writer.write(key + " -> " + str(value) + "\n")
                        
    def findNewName(self, LHS):             # Tested
        new_name = LHS + "'"
        notunique = True
        while(notunique):
            notunique  = False
            for r in self.production_rule:
                if r.__eq__(ProductionRule(new_name)):
                    new_name += "'"
                    notunique = True
        
        # self.non_terminal_symbols.append(new_name)
        return new_name

    def solveNonImmediateLR(self, first, second):           # Tested
        secondLHS = second.getLHS()
        newRHSFirst = []

        for firstRHS in first.getRHS():
            if firstRHS[0].__eq__(secondLHS):
                for secondRHS in second.getRHS():
                    newcurrFirst = secondRHS.copy()
                    remainingFirst = firstRHS.copy()
                    del remainingFirst[0]

                    newcurrFirst.extend(remainingFirst)
                    newRHSFirst.append(newcurrFirst)
            else:
                newRHSFirst.append(firstRHS)
        
        first.setnewRHS(newRHSFirst)

    def solveImmediateLR(self, first):              # Tested
        LHS = first.getLHS()
        newName = self.findNewName(LHS)

        leftRecursive = []
        nonleftRecursive = []

        # Checks if there is left recursion or not
        for rule in first.getRHS():
            if rule[0].__eq__(LHS):
                new = rule.copy()
                del new[0]
                leftRecursive.append(new)
            else:
                nonleftRecursive.append(rule)
        
        # If no left recursion, exit
        if len(leftRecursive) == 0:
            return
        
        self.addNonterminalSymbol(newName)
        changeRuleFirst = []
        newRuleforNewName = []

        if len(nonleftRecursive) == 0:
            wempty = []
            wempty.append(newName)
            changeRuleFirst.append(wempty)

        for beta in nonleftRecursive:
            nonrecursive = beta.copy()
            nonrecursive.append(newName)
            changeRuleFirst.append(nonrecursive)
        
        for alpha in leftRecursive:
            recursive = alpha.copy()
            recursive.append(newName)
            newRuleforNewName.append(recursive)

        # Amends the original rule
        first.setnewRHS(changeRuleFirst)
        Epsilon = []
        Epsilon.append(self.epsilon)
        newRuleforNewName.append(Epsilon)

        # Adds new production rule
        newProductionRule = ProductionRule(newName)
        newProductionRule.setnewRHS(newRuleforNewName)
        self.production_rule.append(newProductionRule)

    def applyAlgoforLeftRecursion(self):            # Tested
        size = len(self.production_rule)

        for i in range(size):
            for j in range(i):
                self.solveNonImmediateLR(self.production_rule[i], self.production_rule[j])
            self.solveImmediateLR(self.production_rule[i])

    def findCommonPrefixforTwoStrings(self, first, second):         #Tested
        if len(first) == 0 or len(second) == 0 or first[0].__eq__(second[0]) == 0:
            # print("-1 returning")
            return -1
    
        small = first.copy()
        large = second.copy()

        if len(small) > len(large):
            small = second
            large = first

        index = 0
        for largestring in large:
            # print("largestring: ", largestring)
            if index == len(small):
                break
            if largestring.__eq__(small[index]) == 0:
                break
            index +=1

        index -= 1
        return index

    def findStringLongestCommonPrefixforArray(self, RHS):           # Tested
        indexwithCommonPrefix = -1
        outerCommonPrefixIndex = sys.maxsize

        for i in range(len(RHS)):
            # print("i: ", i)
            commonPrefixIndex = sys.maxsize
            for j in range(i+1, len(RHS)):
                # print("j: ", j)
                currCommomPrefixIndex = self.findCommonPrefixforTwoStrings(RHS[i], RHS[j])
                if currCommomPrefixIndex >= 0:
                    commonPrefixIndex = min(currCommomPrefixIndex, commonPrefixIndex)

            if commonPrefixIndex == sys.maxsize:
                continue

            if outerCommonPrefixIndex > commonPrefixIndex:
                outerCommonPrefixIndex = commonPrefixIndex
                indexwithCommonPrefix = i

        if indexwithCommonPrefix == -1:
            return None
        
        result = []
        for i in range(outerCommonPrefixIndex+1):
            result.append(RHS[indexwithCommonPrefix][i])

        return result

    def checkRuleStartswithCommonPrefix(self, rule, LongestCommonPrefix):       # Tested
        for i in range(len(LongestCommonPrefix)):
            if len(rule) == i:
                return False
            if rule[i].__eq__(LongestCommonPrefix[i]) == 0:
                return False
        
        return True
        
    def applyAlgoforleftFactoringOnRule(self, productionRule):          # Tested
        # productionRule = ProductionRule()
        # productionRule = production_Rule
        longestCommonPrefix = self.findStringLongestCommonPrefixforArray(productionRule.getRHS())
        if longestCommonPrefix == None:
            return False
        
        LHS = productionRule.getLHS()
        newName = self.findNewName(LHS)
        self.addNonterminalSymbol(newName)

        amendRules = []
        newRulesforNewName = []

        for rule in productionRule.getRHS():
            if self.checkRuleStartswithCommonPrefix(rule, longestCommonPrefix):
                if len(rule) == len(longestCommonPrefix):
                    forepsilon = []
                    forepsilon.append(self.epsilon)
                    newRulesforNewName.append(forepsilon)
                else:
                    toAdd = []
                    for i in range(len(longestCommonPrefix), len(rule)):
                        toAdd.append(rule[i])
                    newRulesforNewName.append(toAdd)

            else:
                amendRules.append(rule)

        forNewName = []
        forNewName.extend(longestCommonPrefix)
        forNewName.append(newName)
        amendRules.append(forNewName)
        
        productionRule.setnewRHS(amendRules)

        newProductionRule = ProductionRule(newName)
        newProductionRule.addRHSall(newRulesforNewName)

        self.toStoreNewRules.append(newProductionRule)
        return True

    toStoreNewRules = []

    def applyAlgoforLeftFactoredGrammar(self):          #Tested
        value = True

        while(value):
            value = False
            self.toStoreNewRules.clear()

            for prodrule in self.production_rule:
                check = self.applyAlgoforleftFactoringOnRule(prodrule)
                value = value or check
            
            self.production_rule.extend(self.toStoreNewRules)

class PredictiveParser(Grammar):                
    def __init__(self):             #Tested
        super().__init__()
        self.parsingTable = {}
        self.stringForOutput = ""

    def createEmptyParsingTable(self):         #Tested
        terminal_symbols = super().getTerminalSymbols()
        non_terminal_symbols = super().getNonTerminalSymbols()

        for non_terminal in non_terminal_symbols:
            self.parsingTable[non_terminal] = {}
            for terminal in terminal_symbols:
                self.parsingTable[non_terminal][terminal] = None

    def addToParsingTable(self, terminal, nonTerminal, productionRule):         # Tested
        # print(nonTerminal)
        # print(terminal)
        self.parsingTable[nonTerminal][terminal] = productionRule

    def addToParsingTableSet(self, terminal, nonTerminal, productionRule):      # Tested
        for symbolTerminal in terminal:
            self.addToParsingTable(symbolTerminal, nonTerminal, productionRule)

    def terminalSymbolsWhereToAddRule(self, LHS, RHS):              #Tested
        result = []
        needToAddFollowSet = True

        for symbol in RHS:
            firstSetOfSymbol = super().getFirstSet(symbol)
            if firstSetOfSymbol == None:
                continue
                
            toAdd = firstSetOfSymbol.copy()
            if super().epsilon not in toAdd:
                needToAddFollowSet = False
                result.extend(toAdd)
                break
            else:
                toAdd.remove(super().epsilon)
                result.extend(toAdd)

        if needToAddFollowSet:
            toAdd = super().getFollowSet(LHS)
            # print(toAdd)
            result.extend(toAdd)

        return result
    
    def createParsingTable(self):               #Tested
        self.createEmptyParsingTable()

        for productionRule in super().getProductionRules():
            LHS = productionRule.getLHS()
            for RHS in productionRule.getRHS():
                terminalSymbolsToAddRule = self.terminalSymbolsWhereToAddRule(LHS, RHS)
                # print(terminalSymbolsToAddRule)
                toAddInTable = ProductionRule(LHS)
                toAddInTable.addRHS(RHS)
                self.addToParsingTableSet(terminalSymbolsToAddRule, LHS, toAddInTable)

    def findLengthOfRule(self, rule):           # Tested
        if rule is None:
            return 4
        return len(str(rule))
    
    def findLengthOfMaxRuleInTable(self):       # Tested
        length = -1
        for nonterminal in super().getNonTerminalSymbols():
            for terminal in super().getTerminalSymbols():
                length = max(length, self.findLengthOfRule(self.parsingTable[nonterminal][terminal]))
        return length
    
    def printParsingTable(self):                   # Tested
        print("Parsing Table: ")
        length = self.findLengthOfMaxRuleInTable() + 2
        # print(length)
        print("   ", end = "")
        for terminal in super().getTerminalSymbols():
            # print(type(terminal))
            t = terminal.center(length)
            print(f"{t}", end = "")
            # print("{:<40}".format(terminal), end = "")

        print()
        print()
        # print("   ", end = "")
        for non_terminal in super().getNonTerminalSymbols():
            print(non_terminal, end = "")
            print("  ", end = "")
            for terminal in super().getTerminalSymbols():
                currRule = self.parsingTable[non_terminal][terminal]
                if currRule ==  None:
                    t = "None".center(length)
                    print(f"{t}", end = "")
                    # print("{:<40}".format("None"), end = "")
                    continue
                t = str(currRule).center(length)    
                print(f"{t}", end = "")            
                # print("{:<40}".format(str(currRule)), end = "")
            print()
        print()

    def printParsingTableToFile(self, path):
        with open(path, 'w') as writer:
            writer.write("Parsing Table: \n")
            lengthOfMaxRuleInTable = self.findLengthOfMaxRuleInTable() + 5
            terminalSymbols = super().getTerminalSymbols()
            # header = ''.join(f"{terminal : {lengthOfMaxRuleInTable}s}" for terminal in terminalSymbols + "\n")
            yeeeee = "Table"
            header = f"{yeeeee:{lengthOfMaxRuleInTable}s}"
            for terminal in terminalSymbols:
                header += f"{terminal:{lengthOfMaxRuleInTable}s}"
            writer.write(header + "\n")

            for nonterminal in super().getNonTerminalSymbols():
                # rule = nonterminal
                rule = f"{nonterminal:{lengthOfMaxRuleInTable}s}"
                for terminal in terminalSymbols:
                    currrule = str(self.parsingTable[nonterminal][terminal]).replace(super().epsilon, 'epsilon')
                    rule += f"{currrule:{lengthOfMaxRuleInTable}s}"
                rule += "\n"
                writer.write(rule)
            
            writer.write("\n")

    def getProductionRuleFromParsingTable(self, nonTerminal, Terminal):     # Tested
        return self.parsingTable[nonTerminal][Terminal]
    
    def createStringFromTokenListRangeInclusive(self, Tokens, left, right):
        str = ""
        for i in range(left, right+1):
            str += Tokens[i].getTokenName()
            str += " "
        return str
    
    def printParsingStepsToFile(self, path, accepted):
        assert self.stringForOutput is not None

        self.stringForOutput.append("The given input text is " + ("ACCEPTED.\n" if accepted else "REJECTED.\n"))

        with open(path, 'w') as writer:
            writer.write("Parsing Steps are the following: \n")
            # writer.write(str(self.stringForOutput))
            for string in self.stringForOutput:
                writer.write(string.replace(super().epsilon, "epsilon"))

    def printStepForParser(self, stack, tokens, indexOnToken, productionRule, step):        # Tested
        # print("Elements of the stack: ", stack)
        self.stringForOutput.append("Elements of the stack: " + str(stack) + "\n")

        matched_input = self.createStringFromTokenListRangeInclusive(tokens, 0, indexOnToken - 1)
        # print("Matched Input: ", matched_input)
        self.stringForOutput.append("Matched Input: " + matched_input + "\n")

        remaining_input = self.createStringFromTokenListRangeInclusive(tokens, indexOnToken, len(tokens) - 1)
        # print("Remaining Input: ", remaining_input)
        self.stringForOutput.append("Remaining Input: " + remaining_input + "\n")

        # print("Production Rule applying: ", productionRule)
        self.stringForOutput.append("Production Rule applying: " + str(productionRule) + "\n")
        if step == Step.PRODUCTION_RULE:
            # print("Production Rule to apply: ", productionRule)
            self.stringForOutput.append("Production Rule to apply: " + productionRule + "\n")
        elif step == Step.MATCHED_INPUT:
            # print("Matched for: ", stack[-1])
            self.stringForOutput.append("Matched for: " + stack[-1] + "\n")

        # print()
        self.stringForOutput.append("\n")

    def parser(self, tokens):                   # Tested
        self.stringForOutput = []                  
        stack = ["$", super().getFirstSymbol()]

        indexOnToken = 0
        while stack[-1] != "$":
            topElement = stack[-1]
            if super().isNonterminalSymbol(topElement):
                ruleToApply = self.getProductionRuleFromParsingTable(topElement, tokens[indexOnToken].getTokenName())
                self.printStepForParser(stack, tokens, indexOnToken, ruleToApply, "PRODUCTION RULE")
                # print()

                if ruleToApply is None:
                    # Error
                    print("Error at parsing: ", tokens[indexOnToken])
                    self.stringForOutput.append("Error at parsing: "+ str(tokens[indexOnToken]) + "\n")
                    return False
                
                stack.pop()

                iterator = iter(ruleToApply.getRHS())
                right = next(iterator)

                for i in range(len(right) -1, -1, -1):
                    if right[i] == super().epsilon:
                        continue
                    stack.append(right[i])

            elif super().isTerminalSymbol(topElement):
                if topElement == tokens[indexOnToken].getTokenName():
                    self.printStepForParser(stack, tokens, indexOnToken, None, "MATCHED INPUT")
                    stack.pop()
                    indexOnToken += 1

                else:
                    #Unmatched
                    print(f"Does not match: {topElement} with {tokens[indexOnToken]}.")
                    self.stringForOutput.append("Does not match: " + str(topElement) + "with" + str(tokens[indexOnToken]) + "\n")
                    return False
                
        return True

class Step(Enum):           # Tested
    PRODUCTION_RULE = 1
    MATCHED_INPUT = 2

class Token:            #Tested
    def __init__(self, tokenName, value):
        self.tokenName = tokenName
        self.value = value

    def getTokenName(self):
        return self.tokenName
    
    def getValue(self):
        return self.value
    
    def __str__(self):
        return f"Token{{tokenName='{self.tokenName}', value='{self.value}'}}"

class Runninglex:           #Tested
    # @staticmethod
    # def runFlexBasedCommand(self):
    #     currRelativepath = Path.cwd()            # returns the current directory
    #     s = str(currRelativepath.absolute())
    #     print("Path: ", s)

    def readFromAllFromFile(path):
        with open(path, 'r') as file:
            return file.read()
        
    def writeToFile(path, content):
        with open(path, 'w') as file:
            file.write(content)

    def runOnCommandLine(pathToDirectory, command):
        process = subprocess.Popen(command, shell = True, cwd = pathToDirectory)
        process.wait()
        exit_code = process.returncode
        print(f"Command exceuted with exit code: {exit_code}")

    def compileFlex(pathToDirectory):
        command  = "flex lex.l"
        Runninglex.runOnCommandLine(pathToDirectory, command)

    def compileLexCProgram(pathToDirectory):
        command = "gcc lex.yy.c -o output"
        Runninglex.runOnCommandLine(pathToDirectory, command)

    def runOutputFile(pathToDirectory):
        command = os.path.join(pathToDirectory, "output")
        Runninglex.runOnCommandLine(pathToDirectory, command)
    
    def compileAndRunFlex(pathToDirectory):
        try:
            Runninglex.compileFlex(pathToDirectory)
        except subprocess.CalledProcessError as e:
            print("Could not compile flex program")
            print(e)
            raise RuntimeError("Could not compile Flex Program")
        
        try:
            Runninglex.compileLexCProgram(pathToDirectory)
        except subprocess.CalledProcessError as e:
            print("Could not compile the lex.yy.c program")
            print(e)
            raise RuntimeError("Could not compile lex.yy.c")

        try:
            Runninglex.runOutputFile(pathToDirectory)
        except subprocess.CalledProcessError as e:
            print("Could not run output program")
            print(e)
            raise RuntimeError("Could not run output Program")

class ReadingInput:
    def readTokensGeneratedByFlex(path):            #Tested
        # print("Path: ", path)

        with open(path, 'r') as file:
            result = []
            for line in file:
                st = line.strip()
                if not st:
                    continue

                splitted_string = st.split(",")
                tokenName = splitted_string[0].strip()
                value = splitted_string[1].strip()
                newToken = Token(tokenName, value)
                result.append(newToken)

        lastToken = Token("$", "$")
        result.append(lastToken)
        return result

    def readAndCreateLL1Grammar(path):          # Tested
        with open(path, 'r') as file:
            grammar = PredictiveParser()

            startSymbol = file.readline().strip()
            grammar.setFirstSymbol(startSymbol)

            nonTerminalString = file.readline().strip()
            nonTerminals = nonTerminalString.split()
            grammar.addAllNonTerminalSymbolFromIterator(nonTerminals)

            terminalString = file.readline().strip()
            terminals = terminalString.split()
            grammar.addAllTerminalSymbolFromIterator(terminals)

            for line in file:
                input_line = line.strip()
                input_line = input_line.replace('Îµ', "ε")
                # for i in range(len(input_line)):
                #     if input_line[i] == 'ε':
                #         input_line[i] = "\u03b5"
                if not input_line:
                    continue
                grammar.addRule(input_line)

        return grammar

class Main:
    homeDirectory = os.path.abspath("")

    def compileAndRunFlex(grammarChoice):
        directoryPath = os.path.join(Main.homeDirectory, "FlexProgram", f"Grammar{grammarChoice}")
        Runninglex.compileAndRunFlex(directoryPath)

    def takeLL1GrammarInput():
        pathToInputGrammar = os.path.join(Main.homeDirectory, "Input", "InputGrammar.txt")
        return ReadingInput.readAndCreateLL1Grammar(pathToInputGrammar)
    
    def takeFlexProgramTokenList(grammarChoice):
        pathToFlexProgram = os.path.join(Main.homeDirectory, "Output", "OutputTokens.txt")
        return ReadingInput.readTokensGeneratedByFlex(pathToFlexProgram)
    
    def deleteOutputDirectory():
        path = os.path.join(Main.homeDirectory, "Output")
        shutil.rmtree(path, ignore_errors = True)
        assert os.path.exists(path) == False

    def createOutputDirectory():
        # try:
        Main.deleteOutputDirectory()
        # except Exception as e:
        #     pass
        outputDirectoryPath = os.path.join(Main.homeDirectory, "Output")
        os.makedirs(outputDirectoryPath)

    def printGrammarWithNoteToFile(grammar, note):
        pathToOutputDirectory = os.path.join(Main.homeDirectory, "Output")
        grammar.printGrammarWithToFile(pathToOutputDirectory, note)

    def printFirstFollowSetToFile(grammar):
        pathToOutputDirectory = os.path.join(Main.homeDirectory, "Output")
        grammar.printFirstAndFollowSetToFile(pathToOutputDirectory, "First Follow Set")

    def printParsingTableToFile(grammar):
        pathToOutputFile = os.path.join(Main.homeDirectory, "Output", "ParsingTable.txt")
        grammar.printParsingTableToFile(pathToOutputFile)

    def printParsingStepsToFile(grammar, parserAccepted):
        pathToOutputFile = os.path.join(Main.homeDirectory, "Output", "ParsingSteps.txt")
        grammar.printParsingStepsToFile(pathToOutputFile, parserAccepted)

    def main():
        # TESTING

        # t1 = PredictiveParser()
        # # t1.addRule("S", [["b", "S", "S", "a", "a", "S"], ["b", "S", "S", "a", "S", "b"], ["b", "S","b"], ["a"]])
        # t1.addRule("S -> b S S a a S | b S S a S b | b S b | a")
        # # t1.addRule("B", [["B", "e"], ["b"]])
        # # print(t1)
        # t1.printGrammar()
        # # t1.printFirstandFollowSet()
        # # t1.applyAlgoforLeftRecursion()
        # # t1.printGrammar()
        # t1.applyAlgoforLeftFactoredGrammar()
        # t1.printGrammar()

        # print(sys.maxsize)

        # # Example usage
        # # Create a token
        # token = Token("Identifier", "example")
        # # Access token properties
        # print(token.getTokenName())  # Output: Identifier
        # print(token.getValue())  # Output: example
        # print(token)  # Output: Token{tokenName='Identifier', value='example'}

        # t = PredictiveParser()
        # t.setFirstSymbol("S")
        # t.addNonterminalSymbol("S")
        # t.addNonterminalSymbol("L")
        # t.addNonterminalSymbol("L'")
        # t.addTerminalSymbol("(")
        # t.addTerminalSymbol(")")
        # t.addTerminalSymbol("a")
        # t.addRule("S -> ( L ) | a")
        # t.addRule("L -> S L'")
        # t.addRule("L' -> ) S L' | ε")
        # t.createEmptyParsingTable()
        # print(t.findLengthOfRule("A"))
        # print(t.getNonTerminalSymbols())
        # print(t.getTerminalSymbols())
        # print(t.getFirstSymbol())

        # t.setFirstSymbol("S")
        # t.addNonterminalSymbol("S")
        # t.addNonterminalSymbol("A")
        # t.addNonterminalSymbol("B")
        # t.addTerminalSymbol("n")
        # t.addTerminalSymbol("+")
        # t.addTerminalSymbol("*")
        # t.addRule("S -> n B")
        # t.addRule("B -> n B A B | ε")
        # t.addRule("A -> + | *")
        # t.applyAlgoforLeftFactoredGrammar()
        # t.computeFirstAndFollowForAllSymbols()
        # print(t.non_terminal_symbols)
        # t.addToParsingTable()
        # t.createParsingTable()
        # print(t.firstSet)
        
        # t.printParsingTable()
        # path = os.getcwd() + "\FlexProgram\Grammar1\outputTokens.txt"
        # print(path)
        # tokens = ReadingInput.readTokensGeneratedByFlex(path)
        # for token in tokens:
        #     print(token)

        # accept = t.parser(tokens)
        # print(accept)
        # print(t.findLengthOfMaxRuleInTable())
        # print(t.computeFirstSetForparticularSymbol("L'"))
        # t.computeFirstSetForAllTerminalSymbols()
        # t.computeFirstSetforAllNonTerminalSymbols()
        # t.computeFirstSetforAllSymbols()
        # print(t.getProductionRulesBasedOnNonTerminal(""))
        # t.printGrammar()
        # print(t.non_terminal_symbols)
        # print()
        # print(t.firstSet)

        # t.computeFollowSetForAllSymbols()

        # print(t.computeFollowSetForNonTerminalSymbol("S"))
        # t.computeFollowSetForAllSymbols()
        # print(t.followSet)

        # # print
        
        # t.printFirstandFollowSet()

        # t = Runninglex()
        # t.runFlexBasedCommand()

        # path = "E:\Acads\Semester 7\Compiler Design\Lab\lab5\Input\InputGrammar.txt"
        # # # t = ReadingInput()
        # readTokensGeneratedByFlex(path)
        # print(readTokensGeneratedByFlex(path))
        # t = Grammar()


######################################################################################################################################################################

        try:
            Main.createOutputDirectory()
        except Exception as e:
            print("Could not create output file.")
            print(e)

        grammarChoice = int(input("Which grammar to apply (1 or 2): "))
        assert grammarChoice == 1 or grammarChoice == 2

        try:
            Main.compileAndRunFlex(grammarChoice)
        except Exception as e:
            print("Could not compile and run flex program.")
            print(e)

        # grammar = PredictiveParser()
        grammar = None
        try:
            grammar = Main.takeLL1GrammarInput()
        except Exception as e:
            print("Unable to read from grammar file.")
            print(e)

        assert grammar is not None

        # print("Input Grammar: ")
        # grammar.printGrammar()

        try:
            Main.printGrammarWithNoteToFile(grammar, "Input Grammar")
        except Exception as e:
            print("Could not write input grammar to output file")
            print(e)

        grammar.applyAlgoforLeftFactoredGrammar()
        grammar.applyAlgoforLeftRecursion()

        # print("The final LL1 Grammar after removing left recursion and finding the equivalentleft factored grammar: ")
        # grammar.printGrammar()

        try:
            Main.printGrammarWithNoteToFile(grammar, "Equivalent Left Factored and Removing left Recursion Grammar")
        except Exception as e:
            print("Could not write Equivalent left Factored and Removing Left Recursion Grammar to output file.")
            print(e)

        grammar.computeFirstAndFollowForAllSymbols()
        # grammar.printFirstandFollowSet()

        try:
            Main.printFirstFollowSetToFile(grammar)
        except Exception as e:
            print("Could not write First-Follow Set to output file.")
            print(e)
            
        # exit(1)

        tokens = None
        try:
            tokens = Main.takeFlexProgramTokenList(grammarChoice)
        except IOError as e:
            print("Unable to read from Flex output file")
            print(e)

        assert tokens is not None

        grammar.createParsingTable()
        # grammar.printParsingTable()

        try:
            Main.printParsingTableToFile(grammar)
        except Exception as e:
            print("Could not write parsing Table to output file.")
            print(e)

        parserAccepted = grammar.parser(tokens)
        try:
            Main.printParsingStepsToFile(grammar, parserAccepted)
        except Exception as e:
            print("Could not write parser steps to output file.")
            print(e)

        if parserAccepted:
            print("The given input text is ACCEPTED.")
        else: 
            print("The given input text is NOT ACCEPTED.")

if __name__ == "__main__":
    Main.main()

# Tested ALL