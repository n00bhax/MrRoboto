/****************************************************************
**  �������ƣ�YS-V0.7����ʶ��ģ����������+YS-SYN6288�����ϳ�
**	CPU: STC11L08XE
**	����22.1184MHZ
**	�����ʣ�9600 bit/S
**	
**  ���ߣ��������ֻ������Ƽ����޹�˾
**  ���ǵĵ��̣�lobot��zone.taobao.com
**  �޸����ڣ�2017.9.26
**  ˵������ͨģʽ��ֱ�ӷ�����ʶ��
/***************************************************************/
#include "config.h"
/************************************************************************************/
//	nAsrStatus ������main�������б�ʾ�������е�״̬������LD3320оƬ�ڲ���״̬�Ĵ���
//	LD_ASR_NONE:		��ʾû������ASRʶ��
//	LD_ASR_RUNING��		��ʾLD3320������ASRʶ����
//	LD_ASR_FOUNDOK:		��ʾһ��ʶ�����̽�������һ��ʶ����
//	LD_ASR_FOUNDZERO:	��ʾһ��ʶ�����̽�����û��ʶ����
//	LD_ASR_ERROR:		��ʾһ��ʶ��������LD3320оƬ�ڲ����ֲ���ȷ��״̬
/***********************************************************************************/
uint8 idata nAsrStatus=0;	
void MCU_init(); 
extern void SYN_FrameInfo(uint8_t Music,uint8_t *HZdata);
void ProcessInt0(); //ʶ������
void delay(unsigned long uldata);
void User_handle(uint8 dat);//�û�ִ�в�������
void Delay200ms();
void UartInit() ;
void WaitTF0();
void runActionGroup() ;
void Led_test(void);//��Ƭ������ָʾ
uint8_t G0_flag=DISABLE;//���б�־��ENABLE:���С�DISABLE:��ֹ���� 
sbit LED=P4^2;//�ź�ָʾ��
sbit BY_PIN = P1^1;

/***********************************************************
* ��    �ƣ� void  main(void)
* ��    �ܣ� ������	�������
* ��ڲ�����  
* ���ڲ�����
* ˵    ���� 					 
* ���÷����� 
**********************************************************/ 
void Sendata();
void  main(void)
{
	uint8 idata nAsrRes;
	uint8 i=0;
	Led_test();
	MCU_init();
	LD_Reset();
  UartInit();
	UartIni(); /*���ڳ�ʼ��*/
	delay(0x2fff);	 //�Լ���ʱ1s���ҵȴ���ʼ��
	nAsrStatus = LD_ASR_NONE;		//	��ʼ״̬��û������ASR


	while(1)
	{
		switch(nAsrStatus)
		{
			case LD_ASR_RUNING:
			case LD_ASR_ERROR:		
				break;
			case LD_ASR_NONE:
			{
				nAsrStatus=LD_ASR_RUNING;
				if (RunASR()==0)	/*	����һ��ASRʶ�����̣�ASR��ʼ����ASR��ӹؼ��������ASR����*/
				{
					SYN_FrameInfo(0,"����");
					nAsrStatus = LD_ASR_ERROR;
				}
				break;
			}
			case LD_ASR_FOUNDOK: /*	һ��ASRʶ�����̽�����ȥȡASRʶ����*/
			{				
				nAsrRes = LD_GetResult();		/*��ȡ���*/
				User_handle(nAsrRes);//�û�ִ�к��� 
				nAsrStatus = LD_ASR_NONE;
				
				break;
			}
			case LD_ASR_FOUNDZERO:
			default:
			{
				nAsrStatus = LD_ASR_NONE;
				break;
			}
		} 			
	}

}
/***********************************************************
* ��    �ƣ� 	 LED�Ʋ���
* ��    �ܣ� ��Ƭ���Ƿ���ָʾ
* ��ڲ����� �� 
* ���ڲ�������
* ˵    ���� 					 
**********************************************************/
void Led_test(void)
{
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
	Delay200ms();
	LED=~ LED;
}
/***********************************************************
* ��    �ƣ� void MCU_init()
* ��    �ܣ� ��Ƭ����ʼ��
* ��ڲ�����  
* ���ڲ�����
* ˵    ���� 					 
* ���÷����� 
**********************************************************/ 
void MCU_init()
{
	P0 = 0xff;
	P1 = 0xff;
	P2 = 0xff;
	P3 = 0xff;
	P4 = 0xff;
	LD_MODE = 0;		//	����MD�ܽ�Ϊ�ͣ�����ģʽ��д
	IE0=1;
	EX0=1;
	EA=1;
}
/***********************************************************
* ��    �ƣ�	��ʱ����
* ��    �ܣ�
* ��ڲ�����  
* ���ڲ�����
* ˵    ���� 					 
* ���÷����� 
**********************************************************/ 
void Delay200us()		//@22.1184MHz
{
	unsigned char i, j;
	_nop_();
	_nop_();
	i = 5;
	j = 73;
	do
	{
		while (--j);
	} while (--i);
}

void  delay(unsigned long uldata)
{
	unsigned int j  =  0;
	unsigned int g  =  0;
	for (j=0;j<5;j++)
	{
		for (g=0;g<uldata;g++)
		{
			_nop_();
			_nop_();
			_nop_();
		}
	}
}

void Delay200ms()		//@22.1184MHz
{
	unsigned char i, j, k;

	i = 17;
	j = 208;
	k = 27;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}
void Delay100ms()		//@22.1184MHz
{
	unsigned char i, j, k;

	i = 9;
	j = 100;
	k = 14;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}
/***********************************************************
* ��    �ƣ� �жϴ�����
* ��    �ܣ�
* ��ڲ�����  
* ���ڲ�����
* ˵    ���� 					 
* ���÷����� 
**********************************************************/

void ExtInt0Handler(void) interrupt 0  
{ 	
	ProcessInt0();				/*	LD3320 �ͳ��ж��źţ�����ASR�Ͳ���MP3���жϣ���Ҫ���жϴ������зֱ���*/
}
/***********************************************************
* ��    �ƣ����ڷ������ݺ���
* ��    �ܣ�
* ��ڲ�����  
* ���ڲ�����
* ˵    ���� 					 
* ���÷�����
************************************************************/
typedef unsigned char uchar;
int i;
uchar code info[] = {0x55,0x55,0x05,0x06,0x01,0x01,0x00};
sbit newTXD = P1^0;//ģ�⴮�ڵķ��Ͷ���ΪP1.0
void UartInit()
{
	AUXR |= 0x40;		//��ʱ��ʱ��1Tģʽ
	TMOD &= 0x0F;		//���ö�ʱ��ģʽ
	TMOD |= 0x10;		//���ö�ʱ��ģʽ
	TL1 = 0x04;		//���ö�ʱ��ֵ
	TH1 = 0xF7;		//���ö�ʱ��ֵ
	TF1 = 0;		//���TF1��־

}
void WaitTF0(void)
{
  while(!TF1);
  TF1=0;
	TL1 = 0x04;		//���ö�ʱ��ֵ
	TH1 = 0xF7;		//���ö�ʱ��ֵ
}
void WByte(uchar input)
{
     //������ʼλ
     uchar j=8;
	   newTXD=(bit)0;
     TR1=1;
    
     WaitTF0();
     //����8λ����λ
     while(j--)
     {
         newTXD=(bit)(input&0x01);      //�ȴ���λ
         WaitTF0();
         input=input>>1;
     }

     //����У��λ(��)

     //���ͽ���λ
     newTXD=(bit)1;
     WaitTF0();
     TR1=0;	 
}    
void Sendata(uint8_t *dat, uint8_t len)
{
		int i = 0;
     for(i=0;i<len;i++)//���ѭ������������
    {
          WByte(dat[i]);
     }
}
/********************��������ú���*************************/
void stopActionGroup()
{
	volatile  uint8_t buf[4];
	buf[0] = 0x55 ;
	buf[1] = 0x55 ;
	buf[2] = 2 ;
	buf[3] = 0x07 ;
	PrintCom(buf, 4) ;
}
void runActionGroup(uint8_t numofAction, uint16_t Times)
{
	static volatile  uint8_t buf[7];
	buf[0] = 0x55 ;
	buf[1] = 0x55 ;
	buf[2] = 5 ;
	buf[3] = 0x06 ;
	buf[4] = (uint8_t)numofAction ;
	buf[5] = GET_LOW_BYTE(Times) ;
	buf[6] = GET_HIGH_BYTE((uint16_t)Times) ;
	PrintCom(buf, 7) ;
	
	Delay200ms();
	Delay200ms();
	Delay200ms();
}
void runXRcmd(uint8_t numofAction,uint8_t Times)
{
	UARTSendByte(0xff);
	UARTSendByte(0x05);
	UARTSendByte(numofAction);
	UARTSendByte(Times);
	UARTSendByte(0xff);
	LED = !LED;
	
	Delay100ms(); 	
SYN_FrameInfo(0,"[v14] ");

}

/***********************************************************
* ��    �ƣ��û�ִ�к��� 
* ��    �ܣ�ʶ��ɹ���ִ�ж������ڴ˽����޸� 
* ��ڲ����� �� 
* ���ڲ�������
* ˵    ���� 					 
**********************************************************/
void 	User_handle(uint8 dat)
{

			 switch(dat)		   /*�Խ��ִ����ز���,�ͻ��޸�*/
			  {
				   
			  	   case 1:	 
						    runXRcmd(1,1);		
							SYN_FrameInfo(0,"[v14]��ɶ");
							break;
				  case 2:	
							runXRcmd(3,1);
							SYN_FrameInfo(0,"��СӰͬѧ��");
						  break;
				  case 3:	 
							SYN_FrameInfo(0,"˭˵�Ҳ�˧");
							runActionGroup(3,1);
							break;
					case 4:	 
							SYN_FrameInfo(0,"�ǵ�Ȼ��");
							runActionGroup(4,1);
							break;
					case 5:	 
							SYN_FrameInfo(0,"�ҳ�����ô�ȣ��˼��˰�������");
							runActionGroup(5,1);
							break;
					case 6:	 
						  SYN_FrameInfo(0,"�����������");
							runActionGroup(6,1);6
							break;
					case 7:	 
					    SYN_FrameInfo(0,"û������");
					    runActionGroup(7,1);
							break;
					case 8:
							SYN_FrameInfo(0,"�������");
							runActionGroup(8,1);
							break;
					case 9:	 
							SYN_FrameInfo(0,"��˵");
							runActionGroup(9,1);
							break;
					case 10:
					 		runXRcmd(3,1);	
							SYN_FrameInfo(0,"[v14] ");	
							Delay200ms();
							SYN_FrameInfo(0,"����Ů���ѣ��ܿɰ�Ŷ");						
							break;
					case 11:	 
							SYN_FrameInfo(0,"˭˵�ұ����ҿɴ�����");
							runActionGroup(11,1);
							break;
					case 12:
							SYN_FrameInfo(0,"�ţ���˵");
							runActionGroup(12,1);
							break;
					case 13:	 
							SYN_FrameInfo(0,"1.414");
							runActionGroup(13,1);
							break;
					case 14:	
							SYN_FrameInfo(0,"4.47");						
							runActionGroup(14,1);
							break;
					case 15:	 
							SYN_FrameInfo(0,"�Ǳ���ģ��ҿ��Ǵ����");
							runActionGroup(15,1);
							break;
					case 16:	 
							runActionGroup(16,1);
							break;
					case 17:	 
							SYN_FrameInfo(0,"��û�и첲û���ȣ����ë����");
							runActionGroup(17,1);
							break;
					case 18:
							runXRcmd(4,1);	
							SYN_FrameInfo(0,"[v14] ");	
							Delay100ms();
							SYN_FrameInfo(0,"�˼�Ҳ��֪���");
							break;
					case 19:	 
							SYN_FrameInfo(0,"�㶺����");
							runActionGroup(19,1);
							break;
					case 20:	
							SYN_FrameInfo(0,"����ټ�����Ҫ����Ŷ");						
							runActionGroup(20,1);
							break;
					default:
						SYN_FrameInfo(0,"������Ϊ����С��");
					  runActionGroup(2,1);
				}	
				BY_PIN = 1;
				while(BY_PIN);
}	 