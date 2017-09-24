#encoding:utf8

from collections import namedtuple
from codecs import open
import sys

Course = namedtuple("Course", ["name", "score", "credit","power"])

class BestDistributionFinder:

    def run(self,record_file):
        "entry function"
        self.__do_init()
        self.__readRecord(record_file)
        self.__calCompulsoriesCreditsAndPower()
        self.__sortOptionalByPower()
        self.__searchByDps()
        try:
            self.displayInTable()   
        except ImportError:
            self.displayInPrint()
            
   
    def __do_init(self):
        self.compulsories, self.pro_electives, self.gen_electives = [], [], []
        self.B1, self.B2 = set(), []
        # Search relevant
        self.best_grade, self.best_B1, self.best_B2 = 0, None, None
        
    def __readRecord(self,file_name):
        '''
        read data from <file_name>, different kinds of courses are split by "***"
        '''
        cur_kind = 0
        with open(file_name, 'r', 'utf8') as f:
            for line in f:
                if line != '' and line is not None:
                    if line.startswith('***'):
                        cur_kind += 1
                        continue
                    name,credit,score = line.strip().split()
                    course = Course(name, float(score), float(credit), float(score) * float(credit))
                    if cur_kind == 1:
                        self.compulsories.append(course)
                    elif cur_kind == 2:
                        self.pro_electives.append(course)
                    else:
                        self.gen_electives.append(course)

    def __calCompulsoriesCreditsAndPower(self):
        '''
        Calculate all complulsories credit and power (basic of B1 list)
        '''
        self.basic_credits = sum(c.credit for c in self.compulsories)
        self.basic_powers = sum(c.credit*c.score for c in self.compulsories)
    
    def __sortOptionalByPower(self):
        self.sorted_electives = self.gen_electives + self.pro_electives
        self.sorted_electives.sort(key = lambda x: x.power, reverse=True)


    def __calculateCurrentGrades(self):
        '''
        Calculate total grade of the current distribution (B1 and B2)
        '''
        b1_credit = sum(c.credit for c in self.B1) + self.basic_credits
        b1_power = sum(c.power for c in self.B1) + self.basic_powers
        b2_size = 0
        self.B2.clear()
        for course in self.sorted_electives:
            if not course in self.B1:
                b2_size += 1
                if b2_size <= 8:
                    self.B2.append(course)
        return b1_power/b1_credit + 0.002 * sum(course.power for course in self.B2)

    def __searchByDps(self):
        if len(self.B1) == 4:
            return
        for course in self.sorted_electives:
            if not course in self.B1:
                self.B1.add(course)
                curr_grade = self.__calculateCurrentGrades()
                if curr_grade > self.best_grade:
                    self.best_grade = curr_grade
                    self.best_B1 = self.B1.copy()
                    self.best_B2 = self.B2.copy()
                self.__searchByDps()
                self.B1.remove(course)
                
    def displayInTable(self):
        import prettytable 
        print('最优总分为：{}\n'.format(self.best_grade))
        print('********************************************')
        print('B1列表\n')
        table1 = prettytable.PrettyTable(["科目","学分","成绩"])
        for course in self.best_B1: 
            table1.add_row([course.name,course.credit,course.score])
        print(table1)

        print('********************************************')
        print('B2列表\n')
        table2 = prettytable.PrettyTable(("科目","学分","成绩"))
        for course in self.best_B2:
            table2.add_row([course.name,course.credit,course.score])
        print(table2)

        print('********************************************')
        print('主修科目\n')
        table3 = prettytable.PrettyTable(("科目","学分","成绩"))    
        for course in self.compulsories:
            table3.add_row([course.name,course.credit,course.score])
        print(table3)
    
    def displayInPrint(self):
        print('最优总分为：{}\n'.format(self.best_grade))
        print('********************************************')
        print('B1列表\n')
        for course in self.best_B1: 
            print('{}\t\t{}\t\t{}'.format(course.name,course.credit,course.score))        
                 
        print('********************************************')
        print('B2列表：\n')
        for course in self.best_B2:
            print('{}\t\t{}\t\t{}'.format(course.name,course.credit,course.score))         
            
        print('********************************************')
        print('主修科目\n')
        for course in self.compulsories:
            print('{}\t\t{}\t\t{}'.format(course.name,course.credit,course.score))            


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('Record file path should be input!')
    record_file = sys.argv[1]
    finder = BestDistributionFinder()
    finder.run(record_file)




                    

                