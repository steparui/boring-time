#-*-coding:utf-8-*-
import os,xlrd
path = "F://GG//05_Server//gameserver//config//table" #文件夹目录  
File_table_h = "xlsx_table_h.txt"
File_table_cpp = "xlsx_table_cpp.txt"
File_cache_h = "cache_h.txt"
File_cache_cpp_path = "cache_cpp_path.txt"
File_cache_cpp_define = "cache_cpp_define.txt"

#生成模板
def get_template_h(filepath, col_names):
        filename = filepath.partition('.')[0]

        classname = "XLSX_"+filename #类名
        unit = filename+"Unit" #单元名
        unitPtr = unit + "Ptr" 
        constUnitPtr = "cosnt"+unitPtr
        data = "" #数据

        #空值返回
        if col_names == None :
                print(filepath)
                return
        
        for col_name in col_names:
                if col_name == None:
                        print(filepath)
                        return
                cell = str(col_name).lower()
                #print(cell)
                data = data + "              uint32 m_" + cell+";\n"
                
        h = ("//////////////////////////////////////////////////////////////////////////\n"
        "// "+classname+"\n"
        "// \n"
        "//////////////////////////////////////////////////////////////////////////\n"
        "class "+classname + " : public XLSXBase\n" 
        "{\n" 
        "	// 不允许直接访问\n" 
        "       class " + unit + "\n"
        "       {\n"
        "       public:\n" 
	""	+data+""
        "       };\n"
        "public:\n"
        "	typedef shared_ptr<"+ unit + "> "+ unitPtr +";\n"
        "	typedef shared_ptr<const "+unit+ "> "+ constUnitPtr +";\n"
        "\n"
        "	"+classname+"(const string& file_name) : XLSXBase(file_name){}\n"
        "	// 资源改变回调接口\n"
        "	virtual bool set_data();\n"
        "	// 填充临时数据\n"
        "	virtual bool stuff_data();\n"
        "	// 释放各项资源\n"
        "	virtual void release(){m_table.clear();}\n"
        "     	// 资源检测回调接口\n"
	"       virtual bool check_data(bool is_modify);\n"
        "	// 查找对象\n"
        "	"+constUnitPtr+" find(const uint32 type);\n"
        "private:\n"
        "	map<uint32,"+ unitPtr+"> m_table;\n"
        "	map<uint32, "+unitPtr+"> m_table_copy;\n"
        "};\n"
        "\n")
        #print(h)
        return h


def get_template_cpp(filepath, col_names):
        filename = filepath.partition('.')[0]
        classname = "XLSX_"+filename #类名
        unit = filename+"Unit" #单元名
        unitPtr = unit + "Ptr" 
        constUnitPtr = "cosnt"+unitPtr
        data = "" #数据
        for col_name in col_names:
                if col_name == None:
                        print(filepath)
                        return

                cell = str(col_name).lower()
                data = data + "              if(!m_parser_xlsx->GetData(i, "+ cell+", unit->m_"+cell+")) get_succ = false;\n"
                
        
        cpp = ("//////////////////////////////////////////////////////////////////////////\n"
        "// "+classname+"\n"
        "// \n"
        "//////////////////////////////////////////////////////////////////////////\n"
        "bool "+classname+"::stuff_data() \n"
	"{\n"
	"	m_table_copy.clear();\n"
	"\n"
	"	for (uint32 i = 0; i < m_parser_xlsx->get_y_count(); i++)\n"
	"	{ \n"
	"		bool get_succ = true;\n"
	"		"+unitPtr+" unit = "+unitPtr+"(new(nothrow)"+ unit+");\n"
        #数据
        ""+data+""
	"	\n"
	"		if (!get_succ)\n"
	"		{\n"
	"			return false;\n"
	"		}\n"
	"\n"
	"		m_table_copy[unit->m_id] = unit;\n"
	"	}\n"
	"	return true;\n"
	"}\n"
	"\n"
	""+classname+"::"+unitPtr+" "+ classname+"::find(uint32 m_id)\n"
	"{\n"
	"	map<uint32, "+unitPtr+">::const_iterator it = m_table.find(m_id);\n"
	"	if(it == m_table.end()) return "+unitPtr+"();\n"
	"\n"
	"	return it->second;\n"
	"}\n"
	"\n"
	"bool "+classname+"::set_data()\n"
	"{\n"
	"	map<uint32, "+unitPtr+">::iterator it_item = m_table_copy.begin();\n"
	"	for (; it_item != m_table_copy.end(); it_item++)\n"
	"	{\n"
	"		map<uint32, rowUnitPtr>::iterator it = m_table.find(it_item->first);\n"
	"		if (it == m_table.end())\n"
	"		{\n"
	"			"+unitPtr+" unit = "+unitPtr+"(new(nothrow)"+unit+");\n"
	"			*unit.get() = *it_item->second.get();\n"
	"			m_table[unit->m_id] = unit;\n"
	"		}\n"
	"		else\n"
	"			*it->second.get() = *it_item->second.get();\n"
	"	}\n"
	"	m_table_copy.clear();\n"
	"\n"
	"	return true;\n"
	"}\n"
        "\n")
        #print(cpp)
        return cpp

#cache_const模板
def get_cache_h(filepath):
        filename = filepath.partition('.')[0]
        classname = "XLSX_"+filename #类名
        dataname = filename[0].lower() + filename[1:]
        result = "	static "+classname+" m_"+dataname+";\n"
        return result

def get_cache_cpp_path(filepath):
        filename = filepath.partition('.')[0]
        classname = "XLSX_"+filename #类名
        dataname = filename[0].lower() + filename[1:]
        result = classname + " CacheConst::m_"+dataname+"(\"config/table/\" + language_branch + \""+filepath+"\");\n"
        return result

def get_cache_cpp_define(filepath):
        filename = filepath.partition('.')[0]
        classname = "XLSX_"+filename #类名
        dataname = filename[0].lower() + filename[1:]
        result = "	m_tables[\""+classname+"\"] = &m_"+ dataname
        return result

#获取列表名
def get_col_name(filepath):
        data = xlrd.open_workbook(filepath)
        table = data.sheets()[0]
        col_names = table.row_values(0)
        #print(col_names)
        return col_names

#得到文件夹下的所有xlsx文件名称
def get_files_name(path):
         
        files= os.listdir(path)  
        result = []
        #遍历
        for file in files:
                if os.path.splitext(file)[1] == '.xlsx':
                        result.append(file)
        return result

#加载文件
def load_file(load_type, filename):
        #打开文件
        file_table_h = open(File_table_h, 'w', encoding="utf-8")
        file_table_cpp = open(File_table_cpp, 'w', encoding="utf-8")
        file_cache_h = open(File_cache_h, 'w', encoding="utf-8")
        file_cache_cpp_path = open(File_cache_cpp_path, 'w', encoding="utf-8")
        file_cache_cpp_define = open(File_cache_cpp_define, 'w', encoding="utf-8")

        h = ""
        cpp = ""
        cache_h = ""
        cache_cpp_path = ""
        cache_cpp_define = ""

        files = get_files_name(path)
        
        #加载全部文件
        if load_type == 1:
                for  file in files:
                        col_names = get_col_name(file)
                        h = h + get_template_h(file, col_names)
                        if h == None:
                                continue

                        cpp = cpp + get_template_cpp(file, col_names)
                        cache_h = cache_h + get_cache_h(file)
                        cache_cpp_path = cache_cpp_path + get_cache_cpp_path(file)
                        cache_cpp_define = cache_cpp_define + get_cache_cpp_define(file)

        #加载单个文件
        elif load_type == 2:
                #是否存在该文件
                filepath = filename + ".xlsx"
                if filepath not in files:
                        return False
                        
                col_names = get_col_name(filepath)
                h = get_template_h(filepath, col_names)
                        
                cpp = get_template_cpp(filepath, col_names)
                cache_h = get_cache_h(filepath)
                cache_cpp_path = get_cache_cpp_path(filepath)
                cache_cpp_define = get_cache_cpp_define(filepath)

                
        #写入文件
        file_table_h.write(h)
        file_table_cpp.write(cpp)
        file_cache_h.write(cache_h)
        file_cache_cpp_path.write(cache_cpp_path)
        file_cache_cpp_define.write(cache_cpp_define)
        
        file_table_h.close()
        file_table_cpp.close()
        file_cache_h.close()
        file_cache_cpp_path.close()
        file_cache_cpp_define.close()

        return True

if __name__ == '__main__':
        testPath ="F://GG//05_Server//gameserver//config//table//ShopTable.xlsx"

        print("请将该文件置于表的当前路径\n")
        while True:
                print("\n请输入 1 == 加载当前全部xlsx文件 | 2 == 加载单个文件 (重新加载将会覆盖文件) \n")
                load_type = input()
                if load_type == "1":
                        #加载全部xlsx文件
                        load_file(1, "")
                elif load_type == "2":
                        while True:
                                print("\n请输入文件名(不要后缀) 0 == 返回上一层\n")
                                filename = input()

                                #返回上一层
                                if filename == "0":
                                        break

                                #加载单个文件
                                result = load_file(2, filename)
                                
                                if result == False:
                                        print("文件名不存在")
                                elif result == True:
                                        break
                else:
                        print("输入不正确")
                
                
        
        
        





        
       
